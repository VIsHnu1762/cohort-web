import { useState, useEffect, useCallback, useRef } from 'react';
import { Loader2, Calendar, TrendingUp, CheckCircle, Clock, XCircle, RefreshCw, ArrowLeft } from 'lucide-react';
import monthlyReportService from '../../services/monthlyReport';
import ProgressBar from '../../components/ProgressBar';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import '../student/MonthlyReport.css';

const StudentMonthlyReport = ({ student, onBack }) => {
  const [reportData, setReportData] = useState(null);
  const [availableMonths, setAvailableMonths] = useState([]);
  const [selectedMonth, setSelectedMonth] = useState(null);
  const [selectedYear, setSelectedYear] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const refreshIntervalRef = useRef(null);

  useEffect(() => {
    if (student) {
      fetchAvailableMonths();

      // Set up auto-refresh every 30 seconds
      refreshIntervalRef.current = setInterval(() => {
        if (selectedMonth && selectedYear) {
          fetchMonthlyReport(true); // Silent refresh
        }
      }, 30000);

      // Cleanup interval on unmount
      return () => {
        if (refreshIntervalRef.current) {
          clearInterval(refreshIntervalRef.current);
        }
      };
    }
  }, [student, selectedMonth, selectedYear]);

  useEffect(() => {
    if (selectedMonth && selectedYear) {
      fetchMonthlyReport();
    }
  }, [selectedMonth, selectedYear]);

  const fetchAvailableMonths = async () => {
    try {
      const data = await monthlyReportService.getAvailableMonthsForStudent(student.id);
      setAvailableMonths(data.months);
      
      // Set current month as default
      if (data.months.length > 0) {
        const currentMonth = data.months[0];
        setSelectedMonth(currentMonth.month);
        setSelectedYear(currentMonth.year);
      }
    } catch (err) {
      console.error('Error fetching available months:', err);
      setError('Failed to load available months');
    }
  };

  const fetchMonthlyReport = async (silent = false) => {
    if (!silent) {
      setLoading(true);
    } else {
      setRefreshing(true);
    }
    setError(null);
    
    try {
      const data = await monthlyReportService.getStudentReport(student.id, selectedMonth, selectedYear);
      setReportData(data);
      setLastUpdated(new Date());
    } catch (err) {
      console.error('Error fetching monthly report:', err);
      if (!silent) {
        setError(err.response?.data?.error || 'Failed to load monthly report');
      }
    } finally {
      if (!silent) {
        setLoading(false);
      } else {
        setRefreshing(false);
      }
    }
  };

  const handleManualRefresh = () => {
    fetchMonthlyReport();
    fetchAvailableMonths();
  };

  const handleMonthChange = (e) => {
    const [year, month] = e.target.value.split('-');
    setSelectedYear(parseInt(year));
    setSelectedMonth(parseInt(month));
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="status-icon completed" />;
      case 'in-progress':
        return <Clock className="status-icon in-progress" />;
      case 'not-started':
        return <XCircle className="status-icon not-started" />;
      default:
        return null;
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'in-progress':
        return 'In Progress';
      case 'not-started':
        return 'Not Started';
      case 'not-applicable':
        return 'N/A';
      default:
        return status;
    }
  };

  const pillarNames = {
    clt: 'CLT (Certificate & Learning)',
    sri: 'SRI (Social Responsibility)',
    cfc: 'CFC (Campus to Corporate)',
    iipc: 'IIPC (Industry Interaction)',
    scd: 'SCD (Software & Coding)',
  };

  if (loading) {
    return (
      <div className="monthly-report-container">
        <div className="loading-container">
          <Loader2 className="spinner" />
          <p>Loading monthly report...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="monthly-report-container">
        <div className="error-container">
          <p>{error}</p>
          <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
            <Button onClick={fetchMonthlyReport}>
              Try Again
            </Button>
            <Button onClick={onBack} variant="secondary">
              <ArrowLeft size={16} /> Back to Students
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="monthly-report-container">
      <div className="monthly-report-header">
        <div className="header-content">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
            <Button onClick={onBack} variant="secondary" style={{ padding: '0.5rem' }}>
              <ArrowLeft size={20} />
            </Button>
            <h1>
              <Calendar className="header-icon" />
              Monthly Report - {student.name}
            </h1>
          </div>
          <p>Track monthly task completion across all pillars for {student.rollNo}</p>
          {lastUpdated && (
            <p className="last-updated">
              Last updated: {lastUpdated.toLocaleTimeString()}
              {refreshing && <span className="refreshing-badge"> (Updating...)</span>}
            </p>
          )}
        </div>
        
        <div className="month-selector">
          <button 
            onClick={handleManualRefresh} 
            className="refresh-button"
            disabled={loading || refreshing}
            title="Refresh data"
          >
            <RefreshCw className={`refresh-icon ${refreshing ? 'spinning' : ''}`} />
          </button>
          <select 
            value={selectedYear && selectedMonth ? `${selectedYear}-${selectedMonth}` : ''}
            onChange={handleMonthChange}
            className="month-select"
          >
            {availableMonths.map((month) => (
              <option key={`${month.year}-${month.month}`} value={`${month.year}-${month.month}`}>
                {month.display}
              </option>
            ))}
          </select>
        </div>
      </div>

      {reportData && (
        <>
          {/* Overall Progress */}
          <GlassCard className={`overall-progress-card ${refreshing ? 'refreshing' : ''}`}>
            <div className="overall-header">
              <div className="overall-title">
                <TrendingUp className="title-icon" />
                <h2>Month {reportData.month} - {reportData.year} Overview</h2>
              </div>
              {getStatusIcon(reportData.overall_progress >= 100 ? 'completed' : reportData.overall_progress > 0 ? 'in-progress' : 'not-started')}
            </div>
            
            <div className="overall-stats">
              <div className="stat-item">
                <span className="stat-label">Overall Progress</span>
                <span className="stat-value">
                  {reportData.overall_progress}%
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Status</span>
                <span className={`stat-value status-${reportData.overall_progress >= 100 ? 'completed' : reportData.overall_progress > 0 ? 'in-progress' : 'not-started'}`}>
                  {getStatusText(reportData.overall_progress >= 100 ? 'completed' : reportData.overall_progress > 0 ? 'in-progress' : 'not-started')}
                </span>
              </div>
            </div>
            
            <ProgressBar 
              progress={reportData.overall_progress} 
              color={reportData.overall_progress === 100 ? '#10b981' : '#3b82f6'}
            />
          </GlassCard>

          {/* Pillar Breakdown */}
          <div className="pillars-grid">
            {Object.entries(reportData.pillars).map(([pillarKey, pillarData]) => (
              <GlassCard key={pillarKey} className="pillar-card">
                <div className="pillar-header">
                  <h3>{pillarNames[pillarKey]}</h3>
                  {getStatusIcon(pillarData.percentage >= 100 ? 'completed' : pillarData.percentage > 0 ? 'in-progress' : 'not-started')}
                </div>
                
                <div className="pillar-stats">
                  <div className="stat-row">
                    <span>Completed:</span>
                    <span className="stat-value-bold">
                      {pillarData.completed} / {pillarData.target}
                    </span>
                  </div>
                </div>
                
                <ProgressBar 
                  progress={pillarData.percentage} 
                  color={pillarData.percentage === 100 ? '#10b981' : '#3b82f6'}
                  size="small"
                />
              </GlassCard>
            ))}
          </div>

          {/* Monthly Requirements Info */}
          <GlassCard className="requirements-card">
            <h3>Monthly Requirements</h3>
            <div className="requirements-list">
              <div className="requirement-item">
                <span className="requirement-pillar">CLT:</span>
                <span>1 certificate upload</span>
              </div>
              <div className="requirement-item">
                <span className="requirement-pillar">CFC:</span>
                <span>3 tasks (Hackathon, BMC, GenAI Project - Internship is optional)</span>
              </div>
              <div className="requirement-item">
                <span className="requirement-pillar">IIPC:</span>
                <span>2 tasks (LinkedIn Post + Connection)</span>
              </div>
              <div className="requirement-item">
                <span className="requirement-pillar">SCD:</span>
                <span>1 LeetCode profile with minimum 10 problems solved</span>
              </div>
            </div>
          </GlassCard>
        </>
      )}
    </div>
  );
};

export default StudentMonthlyReport;

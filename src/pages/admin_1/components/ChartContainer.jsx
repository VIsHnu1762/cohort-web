import React from 'react';
import { motion } from 'framer-motion';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
    ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell,
    RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';
import { useTheme } from '../../../theme/ThemeContext';
import GlassCard from '../../../components/GlassCard';
import './ChartContainer.css';

/**
 * Reusable Chart Container with theme-aware styling
 */
const ChartContainer = ({ title, subtitle, children, delay = 0 }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay }}
            className="chart-container-wrapper"
        >
            <GlassCard variant="large">
                <div className="chart-container">
                    <div className="chart-header">
                        <h3 className="chart-title">{title}</h3>
                        {subtitle && <p className="chart-subtitle">{subtitle}</p>}
                    </div>
                    <div className="chart-content">
                        {children}
                    </div>
                </div>
            </GlassCard>
        </motion.div>
    );
};

/**
 * Monthly Pillar Completion Bar Chart
 */
export const PillarCompletionChart = ({ data, delay }) => {
    const { theme } = useTheme();
    const isDark = theme === 'dark';

    const colors = {
        CLT: '#ffcc00',
        SRI: '#ffcc00',
        CFC: '#42A5F5',
        IIPC: '#66BB6A',
        SCD: '#AB47BC'
    };

    return (
        <ChartContainer
            title="Monthly Pillar Completion"
            subtitle="Completion count across all 5 pillars"
            delay={delay}
        >
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#E5E7EB'} />
                    <XAxis
                        dataKey="month"
                        stroke={isDark ? '#9CA3AF' : '#6B7280'}
                        style={{ fontSize: '0.875rem' }}
                    />
                    <YAxis
                        stroke={isDark ? '#9CA3AF' : '#6B7280'}
                        style={{ fontSize: '0.875rem' }}
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: isDark ? '#1F2937' : '#FFFFFF',
                            border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
                            borderRadius: '8px',
                            color: isDark ? '#F9FAFB' : '#111827'
                        }}
                    />
                    <Legend />
                    {Object.keys(colors).map(pillar => (
                        <Bar key={pillar} dataKey={pillar} fill={colors[pillar]} radius={[8, 8, 0, 0]} />
                    ))}
                </BarChart>
            </ResponsiveContainer>
        </ChartContainer>
    );
};

/**
 * Department/Floor Performance Radar Chart
 */
export const FloorPerformanceChart = ({ data, delay }) => {
    const { theme } = useTheme();
    const isDark = theme === 'dark';

    return (
        <ChartContainer
            title="Floor Performance Comparison"
            subtitle="Performance metrics across different floors"
            delay={delay}
        >
            <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={data}>
                    <PolarGrid stroke={isDark ? '#374151' : '#E5E7EB'} />
                    <PolarAngleAxis
                        dataKey="floor"
                        stroke={isDark ? '#9CA3AF' : '#6B7280'}
                        style={{ fontSize: '0.875rem' }}
                    />
                    <PolarRadiusAxis
                        stroke={isDark ? '#9CA3AF' : '#6B7280'}
                        style={{ fontSize: '0.875rem' }}
                    />
                    <Radar
                        name="Performance"
                        dataKey="performance"
                        stroke="#42A5F5"
                        fill="#42A5F5"
                        fillOpacity={0.6}
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: isDark ? '#1F2937' : '#FFFFFF',
                            border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
                            borderRadius: '8px'
                        }}
                    />
                </RadarChart>
            </ResponsiveContainer>
        </ChartContainer>
    );
};

/**
 * Submission Trend Line Chart
 */
export const SubmissionTrendChart = ({ data, delay }) => {
    const { theme } = useTheme();
    const isDark = theme === 'dark';

    return (
        <ChartContainer
            title="Submission Trend Over Time"
            subtitle="Monthly submission volume"
            delay={delay}
        >
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#E5E7EB'} />
                    <XAxis
                        dataKey="month"
                        stroke={isDark ? '#9CA3AF' : '#6B7280'}
                        style={{ fontSize: '0.875rem' }}
                    />
                    <YAxis
                        stroke={isDark ? '#9CA3AF' : '#6B7280'}
                        style={{ fontSize: '0.875rem' }}
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: isDark ? '#1F2937' : '#FFFFFF',
                            border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
                            borderRadius: '8px'
                        }}
                    />
                    <Legend />
                    <Line
                        type="monotone"
                        dataKey="submissions"
                        stroke="#66BB6A"
                        strokeWidth={3}
                        dot={{ fill: '#66BB6A', r: 5 }}
                        activeDot={{ r: 7 }}
                    />
                </LineChart>
            </ResponsiveContainer>
        </ChartContainer>
    );
};

/**
 * XP Distribution Pie Chart
 */
export const XPDistributionChart = ({ data, delay }) => {
    const { theme } = useTheme();
    const isDark = theme === 'dark';

    const COLORS = ['#ffcc00', '#ffcc00', '#42A5F5', '#66BB6A', '#AB47BC'];

    return (
        <ChartContainer
            title="XP Distribution by Pillar"
            subtitle="Total XP earned per pillar"
            delay={delay}
        >
            <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                    <Pie
                        data={data}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                        outerRadius={100}
                        fill="#8884d8"
                        dataKey="value"
                    >
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                    </Pie>
                    <Tooltip
                        contentStyle={{
                            backgroundColor: isDark ? '#1F2937' : '#FFFFFF',
                            border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
                            borderRadius: '8px'
                        }}
                    />
                </PieChart>
            </ResponsiveContainer>
        </ChartContainer>
    );
};

export default ChartContainer;

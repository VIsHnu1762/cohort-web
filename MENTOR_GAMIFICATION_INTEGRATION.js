/**
 * MENTOR GAMIFICATION INTEGRATION EXAMPLE
 * 
 * This file shows how mentors can integrate gamification controls
 * into their existing dashboard when reviewing student submissions
 */

import React, { useState, useEffect } from 'react';
import gamificationAPI from '../../services/gamification';

/**
 * Example: Adding gamification approval to existing mentor review flow
 * 
 * When mentor approves a submission in existing system,
 * also mark it in gamification system
 */

const MentorSubmissionReview = ({ submission, student }) => {
  const [gamificationData, setGamificationData] = useState(null);

  useEffect(() => {
    loadStudentGamificationProgress();
  }, [student.id]);

  const loadStudentGamificationProgress = async () => {
    try {
      const response = await gamificationAPI.mentor.getStudentProgress(student.id);
      setGamificationData(response.data);
    } catch (error) {
      console.error('Failed to load gamification data:', error);
    }
  };

  /**
   * When mentor approves a submission in existing system,
   * determine which gamification task it corresponds to
   */
  const handleApproveSubmission = async () => {
    // Step 1: Approve in existing system (your current code)
    await approveSubmissionInExistingSystem(submission.id);

    // Step 2: Determine gamification task type and episode
    const { taskType, episodeId } = mapSubmissionToGamificationTask(submission);

    // Step 3: Approve in gamification system
    if (taskType && episodeId) {
      try {
        const response = await gamificationAPI.mentor.approveTask(
          student.id,
          episodeId,
          taskType
        );

        // Show success message
        alert(response.data.message);

        // Reload gamification data
        loadStudentGamificationProgress();
      } catch (error) {
        console.error('Gamification approval failed:', error);
      }
    }
  };

  /**
   * Map existing submission to gamification task
   */
  const mapSubmissionToGamificationTask = (submission) => {
    // Get current season's episodes
    const episodes = gamificationData?.episode_progress || [];

    // Determine task type based on pillar and timing
    let taskType = null;
    let episodeId = null;

    switch (submission.pillar) {
      case 'CLT':
        // CLT is always in Episode 1
        taskType = 'clt';
        episodeId = episodes.find(e => e.episode_details.episode_number === 1)?.episode;
        break;

      case 'CFC':
        // CFC has 3 tasks across episodes 2, 3, 4
        // Determine which task based on submission count or date
        const cfcCount = getApprovedCFCCount(student.id);
        if (cfcCount === 0) {
          taskType = 'cfc_task1';
          episodeId = episodes.find(e => e.episode_details.episode_number === 2)?.episode;
        } else if (cfcCount === 1) {
          taskType = 'cfc_task2';
          episodeId = episodes.find(e => e.episode_details.episode_number === 3)?.episode;
        } else {
          taskType = 'cfc_task3';
          episodeId = episodes.find(e => e.episode_details.episode_number === 4)?.episode;
        }
        break;

      case 'IIPC':
        // IIPC has 2 tasks in episodes 2 and 3
        const iipcCount = getApprovedIIPCCount(student.id);
        if (iipcCount === 0) {
          taskType = 'iipc_task1';
          episodeId = episodes.find(e => e.episode_details.episode_number === 2)?.episode;
        } else {
          taskType = 'iipc_task2';
          episodeId = episodes.find(e => e.episode_details.episode_number === 3)?.episode;
        }
        break;

      case 'SRI':
        // SRI is in Episode 4
        taskType = 'sri';
        episodeId = episodes.find(e => e.episode_details.episode_number === 4)?.episode;
        break;

      case 'SCD':
        // SCD is handled by daily cron, not manual approval
        // But mentor can mark streak as active for current episode
        taskType = 'scd_streak';
        episodeId = getCurrentEpisodeId(episodes);
        break;

      default:
        break;
    }

    return { taskType, episodeId };
  };

  return (
    <div className="mentor-review">
      {/* Your existing review UI */}
      
      {/* Gamification Progress Display */}
      {gamificationData && (
        <div className="gamification-status">
          <h4>Gamification Progress</h4>
          <p>Season Score: {gamificationData.season_score?.total_score || 0}/1500</p>
          
          {gamificationData.episode_progress?.map(ep => (
            <div key={ep.id} className={`episode-status ${ep.status}`}>
              <span>Episode {ep.episode_details.episode_number}</span>
              <span>{ep.status}</span>
              <span>{ep.completion_percentage}%</span>
            </div>
          ))}
        </div>
      )}
      
      <button onClick={handleApproveSubmission}>
        Approve Submission (& Update Gamification)
      </button>
    </div>
  );
};

/**
 * Helper functions (implement based on your existing system)
 */
const approveSubmissionInExistingSystem = async (submissionId) => {
  // Your existing approval logic
  // e.g., api.post(`/submissions/${submissionId}/approve/`)
};

const getApprovedCFCCount = (studentId) => {
  // Count approved CFC submissions for this student in current season
  // This helps determine if it's task 1, 2, or 3
  return 0; // Replace with actual count
};

const getApprovedIIPCCount = (studentId) => {
  // Count approved IIPC submissions for this student in current season
  return 0; // Replace with actual count
};

const getCurrentEpisodeId = (episodes) => {
  // Find the currently active episode (unlocked or in_progress)
  const current = episodes.find(e => 
    e.status === 'unlocked' || e.status === 'in_progress'
  );
  return current?.episode;
};

export default MentorSubmissionReview;

/**
 * ALTERNATIVE APPROACH: Automatic Approval Hook
 * 
 * If you want gamification to auto-update when existing approval happens,
 * create a webhook or signal in your backend:
 */

/*
// In your existing Django submission approval view:

from apps.gamification.services import EpisodeService

def approve_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    submission.status = 'approved'
    submission.save()
    
    # AUTO-TRIGGER GAMIFICATION UPDATE
    try:
        task_type = map_to_gamification_task(submission)
        episode = get_current_episode_for_student(submission.user)
        
        if task_type and episode:
            EpisodeService.mark_task_completed(
                submission.user,
                episode,
                task_type
            )
    except Exception as e:
        logger.error(f"Gamification update failed: {e}")
    
    return Response({'status': 'approved'})
*/

/**
 * INTEGRATION CHECKLIST FOR MENTORS:
 * 
 * [ ] Import gamificationAPI service
 * [ ] Load student gamification progress when viewing submissions
 * [ ] Map your pillars (CLT, CFC, IIPC, SRI, SCD) to gamification tasks
 * [ ] Call approveTask API when approving submissions
 * [ ] Display episode progress in mentor dashboard
 * [ ] Show season score alongside existing metrics
 * [ ] Optionally: Add "Finalize Season" button for completed students
 */

/**
 * MANUAL SEASON FINALIZATION (Optional)
 * 
 * If student completed all 4 episodes but season didn't auto-finalize,
 * mentor can manually trigger it:
 */

const ManualSeasonFinalize = ({ studentId }) => {
  const [loading, setLoading] = useState(false);

  const handleFinalize = async () => {
    if (!confirm('Are you sure you want to finalize this student\'s season?')) {
      return;
    }

    setLoading(true);
    try {
      const response = await gamificationAPI.mentor.finalizeSeason(studentId);
      alert(response.data.message);
      // Refresh data
    } catch (error) {
      alert('Finalization failed: ' + error.response?.data?.error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleFinalize} disabled={loading}>
      {loading ? 'Finalizing...' : 'Finalize Season'}
    </button>
  );
};

/**
 * DISPLAYING STUDENT GAMIFICATION IN MENTOR DASHBOARD
 */

const StudentGamificationCard = ({ studentId }) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    loadData();
  }, [studentId]);

  const loadData = async () => {
    const response = await gamificationAPI.mentor.getStudentProgress(studentId);
    setData(response.data);
  };

  if (!data) return <div>Loading...</div>;

  return (
    <div className="student-gamification-card">
      <h3>{data.student.username}'s Gamification</h3>
      
      <div className="season-info">
        <p>Season: {data.season.name}</p>
        {data.season_score && (
          <p>Score: {data.season_score.total_score}/1500</p>
        )}
      </div>

      <div className="episodes">
        {data.episode_progress.map(ep => (
          <div key={ep.id} className={`episode ${ep.status}`}>
            <h4>{ep.episode_details.name}</h4>
            <div className="progress-bar">
              <div style={{ width: `${ep.completion_percentage}%` }}></div>
            </div>
            <p>{ep.completion_percentage}% Complete</p>
          </div>
        ))}
      </div>
    </div>
  );
};

/**
 * TASK TYPE REFERENCE FOR MAPPING:
 * 
 * Episode 1:
 * - 'clt' → CLT submission
 * - 'scd_streak' → LeetCode streak active
 * 
 * Episode 2:
 * - 'cfc_task1' → First CFC submission
 * - 'iipc_task1' → First IIPC submission
 * - 'scd_streak' → LeetCode streak continues
 * 
 * Episode 3:
 * - 'cfc_task2' → Second CFC submission
 * - 'iipc_task2' → Second IIPC submission
 * - 'scd_streak' → LeetCode streak continues
 * 
 * Episode 4:
 * - 'cfc_task3' → Third CFC submission
 * - 'sri' → SRI submission
 * - 'scd_streak' → LeetCode streak completion
 */

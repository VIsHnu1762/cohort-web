import api from './api';

// Get list of students assigned to mentor
export const getMentorStudents = async () => {
    const response = await api.get('/mentor/students/');
    return response.data;
};

// Get pillar submissions for review
export const getPillarSubmissions = async (pillar, params = {}) => {
    const response = await api.get(`/mentor/pillar/${pillar}/submissions/`, { params });
    return response.data;
};

// Get pillar stats
export const getPillarStats = async (pillar) => {
    const response = await api.get(`/mentor/pillar/${pillar}/stats/`);
    return response.data;
};

// Review a submission
export const reviewSubmission = async (reviewData) => {
    const response = await api.post('/mentor/review/', reviewData);
    return response.data;
};

// Get submission detail
export const getSubmissionDetail = async (pillar, submissionType, submissionId) => {
    const response = await api.get(`/mentor/submission/${pillar}/${submissionType}/${submissionId}/`);
    return response.data;
};

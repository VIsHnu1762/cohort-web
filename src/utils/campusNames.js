/**
 * Campus Name Standardization Utility
 * Maps campus codes to display names for consistent UI presentation
 */

export const CAMPUS_NAMES = {
    TECH: {
        full: 'SNS College of Technology',
        short: 'SNS Tech',
        code: 'TECH',
        type: 'Technology'
    },
    ARTS: {
        full: 'Dr. SNS Rajalakshmi College of Arts and Science',
        short: 'SNS Arts & Science',
        code: 'ARTS',
        type: 'Arts & Science'
    }
};

/**
 * Get full campus name
 * @param {string} campusCode - Campus code (TECH or ARTS)
 * @returns {string} Full campus name
 */
export const getCampusFullName = (campusCode) => {
    return CAMPUS_NAMES[campusCode]?.full || campusCode;
};

/**
 * Get short campus name (for limited space)
 * @param {string} campusCode - Campus code (TECH or ARTS)
 * @returns {string} Short campus name
 */
export const getCampusShortName = (campusCode) => {
    return CAMPUS_NAMES[campusCode]?.short || campusCode;
};

/**
 * Get campus type
 * @param {string} campusCode - Campus code (TECH or ARTS)
 * @returns {string} Campus type
 */
export const getCampusType = (campusCode) => {
    return CAMPUS_NAMES[campusCode]?.type || 'Unknown';
};

/**
 * Get all campus options for selection
 * @returns {Array} Array of campus objects
 */
export const getAllCampuses = () => {
    return Object.values(CAMPUS_NAMES);
};

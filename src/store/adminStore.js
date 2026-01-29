import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

/**
 * Admin Store - Global state management for admin panel
 * Using Zustand for better performance and simpler API than Context
 */

const useAdminStore = create(
  devtools(
    persist(
      (set, get) => ({
        // ===== DASHBOARD STATE =====
        dashboardStats: null,
        loadingStats: false,
        statsError: null,

        setDashboardStats: (stats) => set({ dashboardStats: stats }),
        setLoadingStats: (loading) => set({ loadingStats: loading }),
        setStatsError: (error) => set({ statsError: error }),

        // ===== STUDENTS STATE =====
        students: [],
        selectedStudent: null,
        studentsLoading: false,
        studentsError: null,
        studentsPagination: {
          page: 1,
          pageSize: 20,
          total: 0,
        },

        setStudents: (students) => set({ students }),
        setSelectedStudent: (student) => set({ selectedStudent: student }),
        setStudentsLoading: (loading) => set({ studentsLoading: loading }),
        setStudentsError: (error) => set({ studentsError: error }),
        setStudentsPagination: (pagination) =>
          set({ studentsPagination: { ...get().studentsPagination, ...pagination } }),

        // ===== MENTORS STATE =====
        mentors: [],
        selectedMentor: null,
        mentorsLoading: false,
        mentorsError: null,
        mentorsPagination: {
          page: 1,
          pageSize: 20,
          total: 0,
        },

        setMentors: (mentors) => set({ mentors }),
        setSelectedMentor: (mentor) => set({ selectedMentor: mentor }),
        setMentorsLoading: (loading) => set({ mentorsLoading: loading }),
        setMentorsError: (error) => set({ mentorsError: error }),
        setMentorsPagination: (pagination) =>
          set({ mentorsPagination: { ...get().mentorsPagination, ...pagination } }),

        // ===== FLOORS STATE =====
        floors: [],
        selectedFloor: null,
        floorsLoading: false,
        floorsError: null,

        setFloors: (floors) => set({ floors }),
        setSelectedFloor: (floor) => set({ selectedFloor: floor }),
        setFloorsLoading: (loading) => set({ floorsLoading: loading }),
        setFloorsError: (error) => set({ floorsError: error }),

        // ===== SUBMISSIONS STATE =====
        submissions: [],
        selectedSubmission: null,
        submissionsLoading: false,
        submissionsError: null,
        submissionsPagination: {
          page: 1,
          pageSize: 50,
          total: 0,
        },
        submissionsFilters: {
          pillar: '',
          mentor: '',
          floor: '',
          status: '',
          dateFrom: '',
          dateTo: '',
        },

        setSubmissions: (submissions) => set({ submissions }),
        setSelectedSubmission: (submission) => set({ selectedSubmission: submission }),
        setSubmissionsLoading: (loading) => set({ submissionsLoading: loading }),
        setSubmissionsError: (error) => set({ submissionsError: error }),
        setSubmissionsPagination: (pagination) =>
          set({ submissionsPagination: { ...get().submissionsPagination, ...pagination } }),
        setSubmissionsFilters: (filters) =>
          set({ submissionsFilters: { ...get().submissionsFilters, ...filters } }),
        clearSubmissionsFilters: () =>
          set({
            submissionsFilters: {
              pillar: '',
              mentor: '',
              floor: '',
              status: '',
              dateFrom: '',
              dateTo: '',
            },
          }),

        // ===== LEADERBOARD STATE =====
        leaderboard: [],
        leaderboardLoading: false,
        leaderboardError: null,

        setLeaderboard: (leaderboard) => set({ leaderboard }),
        setLeaderboardLoading: (loading) => set({ leaderboardLoading: loading }),
        setLeaderboardError: (error) => set({ leaderboardError: error }),

        // ===== NOTIFICATIONS STATE =====
        notifications: [],
        notificationsLoading: false,
        notificationsError: null,

        setNotifications: (notifications) => set({ notifications }),
        setNotificationsLoading: (loading) => set({ notificationsLoading: loading }),
        setNotificationsError: (error) => set({ notificationsError: error }),
        addNotification: (notification) =>
          set({ notifications: [notification, ...get().notifications] }),

        // ===== SETTINGS STATE =====
        settings: null,
        settingsLoading: false,
        settingsError: null,

        setSettings: (settings) => set({ settings }),
        setSettingsLoading: (loading) => set({ settingsLoading: loading }),
        setSettingsError: (error) => set({ settingsError: error }),

        // ===== ANALYTICS STATE =====
        analytics: null,
        analyticsLoading: false,
        analyticsError: null,

        setAnalytics: (analytics) => set({ analytics }),
        setAnalyticsLoading: (loading) => set({ analyticsLoading: loading }),
        setAnalyticsError: (error) => set({ analyticsError: error }),

        // ===== UI STATE =====
        sidebarCollapsed: false,
        toggleSidebar: () => set({ sidebarCollapsed: !get().sidebarCollapsed }),
        setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),

        // Modal states
        modals: {
          studentDetail: false,
          mentorDetail: false,
          submissionDetail: false,
          createStudent: false,
          createMentor: false,
          createFloor: false,
          editPillarRules: false,
          sendAnnouncement: false,
        },

        openModal: (modalName) =>
          set({ modals: { ...get().modals, [modalName]: true } }),
        closeModal: (modalName) =>
          set({ modals: { ...get().modals, [modalName]: false } }),
        closeAllModals: () =>
          set({
            modals: Object.keys(get().modals).reduce((acc, key) => {
              acc[key] = false;
              return acc;
            }, {}),
          }),

        // ===== RESET FUNCTIONS =====
        resetStudents: () =>
          set({
            students: [],
            selectedStudent: null,
            studentsLoading: false,
            studentsError: null,
          }),

        resetMentors: () =>
          set({
            mentors: [],
            selectedMentor: null,
            mentorsLoading: false,
            mentorsError: null,
          }),

        resetSubmissions: () =>
          set({
            submissions: [],
            selectedSubmission: null,
            submissionsLoading: false,
            submissionsError: null,
          }),

        resetAll: () =>
          set({
            dashboardStats: null,
            students: [],
            mentors: [],
            floors: [],
            submissions: [],
            leaderboard: [],
            notifications: [],
            settings: null,
            analytics: null,
            selectedStudent: null,
            selectedMentor: null,
            selectedFloor: null,
            selectedSubmission: null,
          }),
      }),
      {
        name: 'admin-storage',
        partialize: (state) => ({
          sidebarCollapsed: state.sidebarCollapsed,
          submissionsFilters: state.submissionsFilters,
        }),
      }
    ),
    {
      name: 'AdminStore',
    }
  )
);

export default useAdminStore;

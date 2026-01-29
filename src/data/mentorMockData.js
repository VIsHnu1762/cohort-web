// Mock data for Mentor Panel - Replace with API calls when backend is ready

export const mentorProfile = {
  id: 1,
  name: "Dr. Priya Sharma",
  email: "priya.sharma@college.edu",
  avatar: null,
  department: "Computer Science",
  assignedFloors: ["Floor 1", "Floor 2"],
  totalStudents: 24,
  joinedDate: "2024-01-15"
};

export const dashboardStats = {
  totalStudents: 24,
  pendingSubmissions: 18,
  approvedThisWeek: 42,
  rejectedThisWeek: 5,
  floorOKRCompletion: 68,
  pillarStats: [
    { pillar: "CLT", completed: 18, total: 24, percentage: 75 },
    { pillar: "SRI", completed: 12, total: 24, percentage: 50 },
    { pillar: "CFC", completed: 20, total: 24, percentage: 83 },
    { pillar: "IIPC", completed: 15, total: 24, percentage: 62 },
    { pillar: "SCD", completed: 10, total: 24, percentage: 42 }
  ],
  monthlyTrends: [
    { month: "Aug", submissions: 45, approved: 38, rejected: 7 },
    { month: "Sep", submissions: 52, approved: 45, rejected: 7 },
    { month: "Oct", submissions: 61, approved: 53, rejected: 8 },
    { month: "Nov", submissions: 58, approved: 51, rejected: 7 },
    { month: "Dec", submissions: 48, approved: 42, rejected: 6 }
  ]
};

export const studentsList = [
  {
    id: 1,
    name: "Rahul Kumar",
    email: "rahul.kumar@student.edu",
    rollNumber: "CS2101",
    floor: "Floor 1",
    avatar: null,
    overallProgress: 72,
    xp: 1250,
    pillars: {
      clt: { completed: 3, total: 4, percentage: 75, status: "on-track" },
      sri: { completed: 2, total: 3, percentage: 67, status: "on-track" },
      cfc: { completed: 4, total: 5, percentage: 80, status: "on-track" },
      iipc: { completed: 2, total: 3, percentage: 67, status: "on-track" },
      scd: { completed: 1, total: 2, percentage: 50, status: "needs-attention" }
    },
    lastActivity: "2024-12-12T10:30:00Z",
    pendingSubmissions: 3,
    status: "active"
  },
  {
    id: 2,
    name: "Priya Patel",
    email: "priya.patel@student.edu",
    rollNumber: "CS2102",
    floor: "Floor 1",
    avatar: null,
    overallProgress: 85,
    xp: 1580,
    pillars: {
      clt: { completed: 4, total: 4, percentage: 100, status: "excellent" },
      sri: { completed: 3, total: 3, percentage: 100, status: "excellent" },
      cfc: { completed: 5, total: 5, percentage: 100, status: "excellent" },
      iipc: { completed: 2, total: 3, percentage: 67, status: "on-track" },
      scd: { completed: 1, total: 2, percentage: 50, status: "needs-attention" }
    },
    lastActivity: "2024-12-13T09:15:00Z",
    pendingSubmissions: 1,
    status: "active"
  },
  {
    id: 3,
    name: "Arjun Singh",
    email: "arjun.singh@student.edu",
    rollNumber: "CS2103",
    floor: "Floor 2",
    avatar: null,
    overallProgress: 45,
    xp: 680,
    pillars: {
      clt: { completed: 1, total: 4, percentage: 25, status: "behind" },
      sri: { completed: 1, total: 3, percentage: 33, status: "behind" },
      cfc: { completed: 2, total: 5, percentage: 40, status: "behind" },
      iipc: { completed: 1, total: 3, percentage: 33, status: "behind" },
      scd: { completed: 0, total: 2, percentage: 0, status: "behind" }
    },
    lastActivity: "2024-12-10T14:20:00Z",
    pendingSubmissions: 6,
    status: "behind-schedule"
  }
];

export const submissions = {
  clt: [
    {
      id: "clt_001",
      studentId: 1,
      studentName: "Rahul Kumar",
      studentEmail: "rahul.kumar@student.edu",
      rollNumber: "CS2101",
      floor: "Floor 1",
      submissionType: "Project Documentation",
      title: "E-Commerce Website Development",
      description: "Full-stack e-commerce platform with payment integration",
      submittedDate: "2024-12-12T10:30:00Z",
      status: "pending",
      evidence: {
        type: "link",
        url: "https://github.com/rahul/ecommerce-project",
        screenshots: []
      },
      previousFeedback: null
    },
    {
      id: "clt_002",
      studentId: 2,
      studentName: "Priya Patel",
      studentEmail: "priya.patel@student.edu",
      rollNumber: "CS2102",
      floor: "Floor 1",
      submissionType: "Learning Reflection",
      title: "React Hooks Deep Dive",
      description: "Comprehensive study and implementation of React Hooks patterns",
      submittedDate: "2024-12-11T15:45:00Z",
      status: "approved",
      evidence: {
        type: "document",
        url: "https://docs.google.com/document/d/xyz",
        screenshots: []
      },
      mentorFeedback: "Excellent work! Shows deep understanding of React concepts.",
      reviewedDate: "2024-12-12T09:00:00Z",
      reviewedBy: "Dr. Priya Sharma"
    }
  ],
  sri: [
    {
      id: "sri_001",
      studentId: 1,
      studentName: "Rahul Kumar",
      studentEmail: "rahul.kumar@student.edu",
      rollNumber: "CS2101",
      floor: "Floor 1",
      submissionType: "Community Service",
      title: "Teaching Programming to Rural Students",
      description: "Conducted 5 sessions teaching Python basics to 20 students",
      submittedDate: "2024-12-10T11:00:00Z",
      status: "pending",
      evidence: {
        type: "images",
        screenshots: ["session1.jpg", "session2.jpg", "certificate.pdf"]
      },
      hoursSpent: 15,
      beneficiaries: 20
    }
  ],
  cfc: [
    {
      id: "cfc_001",
      studentId: 2,
      studentName: "Priya Patel",
      studentEmail: "priya.patel@student.edu",
      rollNumber: "CS2102",
      floor: "Floor 1",
      submissionType: "Hackathon Participation",
      title: "Smart City Hackathon - Winner",
      description: "Developed IoT-based traffic management system",
      submittedDate: "2024-12-09T16:30:00Z",
      status: "approved",
      evidence: {
        type: "link",
        url: "https://devpost.com/software/smart-traffic",
        screenshots: ["certificate.jpg", "project_demo.mp4"]
      },
      achievement: "1st Place",
      teamSize: 4,
      mentorFeedback: "Outstanding achievement! Well done on the hackathon win.",
      reviewedDate: "2024-12-10T10:00:00Z"
    }
  ],
  iipc: [
    {
      id: "iipc_001",
      studentId: 1,
      studentName: "Rahul Kumar",
      studentEmail: "rahul.kumar@student.edu",
      rollNumber: "CS2101",
      floor: "Floor 1",
      submissionType: "LinkedIn Post",
      title: "AI in Healthcare - Future Perspectives",
      description: "Published article on LinkedIn about AI applications in healthcare",
      submittedDate: "2024-12-11T14:00:00Z",
      status: "pending",
      evidence: {
        type: "link",
        url: "https://linkedin.com/posts/rahul-kumar/ai-healthcare",
        metrics: {
          likes: 45,
          comments: 12,
          shares: 8
        }
      },
      characterCount: 850,
      hashtagCount: 5
    }
  ],
  scd: [
    {
      id: "scd_001",
      studentId: 2,
      studentName: "Priya Patel",
      studentEmail: "priya.patel@student.edu",
      rollNumber: "CS2102",
      floor: "Floor 1",
      submissionType: "LeetCode Progress",
      title: "100 LeetCode Problems Solved",
      description: "Completed 100 medium-level problems with focus on dynamic programming",
      submittedDate: "2024-12-08T12:00:00Z",
      status: "approved",
      evidence: {
        type: "link",
        url: "https://leetcode.com/priya-patel",
        screenshots: ["leetcode_profile.png", "progress_chart.png"]
      },
      problemsSolved: 100,
      difficulty: "Medium",
      mentorFeedback: "Great progress! Focus on hard problems next.",
      reviewedDate: "2024-12-09T11:00:00Z"
    }
  ]
};

export const floorAnalytics = {
  "Floor 1": {
    totalStudents: 12,
    okrCompletion: 75,
    averageXP: 1350,
    pillarBreakdown: [
      { pillar: "CLT", completion: 80 },
      { pillar: "SRI", completion: 70 },
      { pillar: "CFC", completion: 85 },
      { pillar: "IIPC", completion: 65 },
      { pillar: "SCD", completion: 55 }
    ],
    topPerformers: [
      { name: "Priya Patel", xp: 1580, progress: 85 },
      { name: "Amit Verma", xp: 1450, progress: 78 },
      { name: "Sneha Reddy", xp: 1420, progress: 76 }
    ],
    needsAttention: [
      { name: "Vikram Rao", xp: 680, progress: 42 }
    ]
  },
  "Floor 2": {
    totalStudents: 12,
    okrCompletion: 61,
    averageXP: 1180,
    pillarBreakdown: [
      { pillar: "CLT", completion: 70 },
      { pillar: "SRI", completion: 58 },
      { pillar: "CFC", completion: 68 },
      { pillar: "IIPC", completion: 52 },
      { pillar: "SCD", completion: 48 }
    ],
    topPerformers: [
      { name: "Karthik Nair", xp: 1380, progress: 72 },
      { name: "Divya Menon", xp: 1320, progress: 70 }
    ],
    needsAttention: [
      { name: "Arjun Singh", xp: 680, progress: 45 },
      { name: "Rohan Das", xp: 720, progress: 48 }
    ]
  }
};

export const notifications = [
  {
    id: 1,
    type: "submission",
    message: "Rahul Kumar submitted a new CLT project",
    timestamp: "2024-12-12T10:30:00Z",
    read: false,
    action: "/mentor/submissions/clt"
  },
  {
    id: 2,
    type: "deadline",
    message: "Monthly evaluation deadline in 3 days",
    timestamp: "2024-12-11T09:00:00Z",
    read: false,
    action: null
  },
  {
    id: 3,
    type: "performance",
    message: "3 students behind schedule need attention",
    timestamp: "2024-12-10T14:00:00Z",
    read: true,
    action: "/mentor/students?filter=behind"
  }
];

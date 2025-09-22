# Single-Page Admin Dashboard for Diabetics Prediction App - Development Prompt

## Project Overview
Build a comprehensive single-page admin dashboard for the diabetics prediction ML application. This should be one unified page that displays all essential admin functions, ML model management, user analytics, and system monitoring in a well-organized layout with sections/widgets. Use the existing color palette and maintain consistency with the current design system.

## Technical Stack
- **Framework**: React with Vite (matching existing setup)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React for consistent iconography
- **Charts**: Recharts for data visualization
- **Layout**: Single-page dashboard with organized sections/cards

## Color Palette (Use Existing)
- **Primary Navy**: #27548A (main brand color, headers, primary actions)
- **Secondary Sea**: #183B4E (section headers, important elements)  
- **Accent Gold**: #DDA853 (highlights, important metrics, notifications)
- **Background Beige**: #F3F3E0 (page background)
- **Pure White**: #FFFFFF (card backgrounds, form inputs)
- **Text Colors**: #183B4E for headings, #27548A for links, #374151 for body text

## Single-Page Dashboard Layout

### Header Section
- **App Logo/Title**: "Admin Dashboard - Diabetes Prediction"
- **Admin Profile**: Avatar, name, role
- **Quick Actions**: Logout button, notifications bell
- **Real-time Status**: System health indicator

### Main Dashboard Content (Single Page with Sections)

## Dashboard Sections Layout

### 1. Key Metrics Overview (Top Row Cards)
**4-Column Metric Cards:**
- **Total Users**: 12,547 users (+12% this month)
- **Active Today**: 1,823 users 
- **Current Model Accuracy**: 84.7% (Model v2.1)
- **Training Status**: 1 job running, 2 completed today

### 2. ML Model Management Section
**Left Half - Current Production Model:**
- Model name, version, accuracy
- Deployment date and status
- Quick actions: View details, Roll back, Deploy new version

**Right Half - Model Training:**
- Active training jobs with progress bars
- Quick start new training with dataset selector
- Recent training history (last 5 jobs)

### 3. Dataset Management Section
**Dataset Upload Area:**
- Drag-and-drop file upload zone
- Supported formats: CSV, JSON, Excel
- Upload progress and validation status

**Dataset List:**
- Table showing recent datasets (name, size, rows, upload date, status)
- Actions: Preview, Download, Use for training

### 4. User Analytics Section
**Left Side - User Charts:**
- User registration trend (last 30 days) - Line chart
- Risk level distribution - Donut chart

**Right Side - User Management:**
- Recent user registrations table
- Quick user search
- User status summary (Active, Inactive, High-risk)

### 5. Predictions Analytics Section
**Charts Row:**
- Predictions made over time - Area chart
- Prediction accuracy trend - Line chart
- Risk factor distribution - Bar chart

### 6. System Monitoring Section
**Bottom Row:**
- System health status
- Recent activity log
- Alerts and notifications
- Quick system actions

## Component Structure (Single Page)
```
src/admin/
├── pages/
│   └── AdminDashboard.jsx (SINGLE PAGE)
├── components/
│   ├── dashboard/
│   │   ├── MetricsCards.jsx
│   │   ├── ModelManagementSection.jsx
│   │   ├── DatasetSection.jsx
│   │   ├── UserAnalyticsSection.jsx
│   │   ├── PredictionsSection.jsx
│   │   └── SystemMonitoringSection.jsx
│   ├── ui/
│   │   ├── StatCard.jsx
│   │   ├── DataTable.jsx
│   │   ├── Chart.jsx
│   │   ├── FileUpload.jsx
│   │   ├── ProgressBar.jsx
│   │   ├── Badge.jsx
│   │   └── Modal.jsx
│   └── charts/
│       ├── LineChart.jsx
│       ├── AreaChart.jsx
│       ├── BarChart.jsx
│       └── DonutChart.jsx
└── hooks/
    ├── useAdminData.jsx
    └── useRealTimeUpdates.jsx
```

## Detailed Section Specifications

### Metrics Cards Section
```jsx
// 4 cards in a row
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
  <StatCard title="Total Users" value="12,547" change="+12%" />
  <StatCard title="Active Today" value="1,823" />
  <StatCard title="Model Accuracy" value="84.7%" status="good" />
  <StatCard title="Training Jobs" value="1 Active" />
</div>
```

### ML Model Section
**Features to Include:**
- Current model card with key metrics
- Training job progress with real-time updates
- Quick training starter with dataset dropdown
- Model comparison widget
- One-click model deployment

### Dataset Section
**Features to Include:**
- Large drag-drop upload area
- File validation and preview
- Dataset quality indicators
- Recent datasets table with actions
- Data preprocessing status

### User Analytics Section
**Features to Include:**
- Interactive charts showing user trends
- Quick user search and filter
- Recent registrations list
- High-risk users alert panel

### Predictions Section
**Features to Include:**
- Prediction volume trends
- Accuracy over time tracking
- Risk distribution visualization
- Recent predictions activity

### System Monitoring Section
**Features to Include:**
- System health status indicators
- Recent admin activity log
- Alert notifications panel
- Quick system maintenance actions

## Mock Data Structure
```javascript
const dashboardData = {
  metrics: {
    totalUsers: 12547,
    activeToday: 1823,
    modelAccuracy: 0.847,
    trainingJobs: { active: 1, completed: 2 }
  },
  currentModel: {
    name: "Diabetes Risk Model v2.1",
    version: "2.1.0",
    accuracy: 0.847,
    status: "Production",
    deployedDate: "2024-03-15"
  },
  trainingJobs: [
    {
      id: 1,
      modelName: "Diabetes Risk Model v2.2",
      status: "Training",
      progress: 67,
      accuracy: 0.821,
      startTime: "2024-03-20 10:30"
    }
  ],
  datasets: [
    {
      id: 1,
      name: "diabetes_march_2024.csv",
      size: "2.3 MB",
      rows: 10500,
      uploadDate: "2024-03-20",
      status: "Ready"
    }
  ],
  recentUsers: [
    {
      id: 1,
      name: "John Doe",
      email: "john@example.com",
      registrationDate: "2024-03-20",
      riskLevel: "Medium"
    }
  ]
}
```

## Layout Specifications

### Responsive Grid Layout
```jsx
<div className="min-h-screen bg-[#F3F3E0] p-6">
  {/* Header */}
  <header className="mb-8">...</header>
  
  {/* Metrics Cards */}
  <section className="mb-8">...</section>
  
  {/* Two-column layout for main sections */}
  <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-8">
    <ModelManagementSection />
    <DatasetSection />
  </div>
  
  {/* Full-width analytics */}
  <section className="mb-8">
    <UserAnalyticsSection />
  </section>
  
  {/* Predictions analytics */}
  <section className="mb-8">
    <PredictionsSection />
  </section>
  
  {/* System monitoring */}
  <footer>
    <SystemMonitoringSection />
  </footer>
</div>
```

## Interactive Features

### Real-time Updates
- Auto-refresh metrics every 30 seconds
- Live training progress updates
- Real-time notification alerts
- Live user activity feed

### Quick Actions
- Start training job with one click
- Upload dataset with drag-drop
- Quick user search across all data
- Instant model deployment
- Export data/reports

### Modal Interactions
- Dataset preview modal
- User details modal
- Training configuration modal
- Model comparison modal

## Design Requirements

### Visual Hierarchy
- **Section Headers**: Large, bold text in #183B4E
- **Cards**: White backgrounds with subtle shadows
- **Charts**: Clean, colorful visualizations using brand colors
- **Spacing**: Consistent 6-8 unit spacing between sections

### Responsive Design
- **Desktop**: Full multi-column layout
- **Tablet**: 2-column responsive grid
- **Mobile**: Single column stacked layout

## Success Criteria
- All admin functions accessible from single page
- Quick overview of system health and performance
- Easy ML model and dataset management
- Real-time monitoring and alerts
- Professional healthcare-appropriate design
- Fast loading and smooth interactions
- Mobile-responsive design

## Key Features Summary
✅ **Single Page** - Everything in one unified view  
✅ **ML Operations** - Model training, dataset upload, monitoring  
✅ **User Management** - Analytics, search, recent activity  
✅ **Real-time Updates** - Live metrics and training progress  
✅ **Interactive Charts** - Visual data representation  
✅ **Quick Actions** - One-click operations for common tasks  
✅ **Professional Design** - Healthcare-appropriate aesthetic  
✅ **Mobile Responsive** - Works on all devices  

Build this as a comprehensive single-page dashboard that gives administrators complete visibility and control over the diabetes prediction ML application in one unified, professional interface.
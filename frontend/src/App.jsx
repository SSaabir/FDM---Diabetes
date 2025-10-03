import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { ProtectedRoute, AdminOnlyRoute, SuperAdminOnlyRoute } from "@/components/ProtectedRoute";
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import FAQ from "./pages/FAQ";
import NotFound from "./pages/NotFound";
import AdminDashboard from "./admin/pages/AdminDashboard";
import AddAdminForm from "./admin/pages/AddAdminForm";
import AboutUs from './pages/AboutUs.jsx';
import Home from './pages/Home.jsx';
import Chat from './pages/Chat.jsx';
import Prediction from './pages/Prediction.jsx';
import Profile from './pages/Profile.jsx';
import ProfileEdit from './pages/ProfileEdit.jsx';
import Header from './components/Header.jsx';
import Footer from './components/Footer.jsx';
import TermsAndConditions from './pages/TermsAndConditions.jsx';
import ContactUs from "./pages/ContactUs.jsx";
import Dashboard from "./pages/Dashboard.jsx";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AuthProvider>
          <Header />
          <Routes>
            <Route path="/contact" element={<ContactUs />} />
            <Route path="/terms" element={<TermsAndConditions />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/faq" element={<FAQ />} />
            
            {/* Admin Routes - Properly Protected */}
            <Route 
              path="/admindashboard" 
              element={
                <AdminOnlyRoute>
                  <AdminDashboard />
                </AdminOnlyRoute>
              } 
            />
            <Route 
              path="/admin/dashboard" 
              element={
                <AdminOnlyRoute>
                  <AdminDashboard />
                </AdminOnlyRoute>
              } 
            />
            <Route 
              path="/admin/add-admin" 
              element={
                <SuperAdminOnlyRoute>
                  <AddAdminForm />
                </SuperAdminOnlyRoute>
              } 
            />
            <Route 
              path="/admin" 
              element={
                <AdminOnlyRoute>
                  <AdminDashboard />
                </AdminOnlyRoute>
              } 
            />
            
            {/* User Routes - Protected */}
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/profile" 
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/profile/edit" 
              element={
                <ProtectedRoute>
                  <ProfileEdit />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/assessment" 
              element={
                <ProtectedRoute>
                  <Prediction />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/prediction" 
              element={
               
                  <Prediction />
               
              } 
            />
            <Route 
              path="/chat" 
              element={
                <ProtectedRoute>
                  <Chat />
                </ProtectedRoute>
              } 
            />
            
            {/* Public Routes */}
            <Route path="/about" element={<AboutUs />} />
            <Route path="/aboutus" element={<AboutUs />} />
            <Route path="/" element={<Home />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
          <Footer />
        </AuthProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;

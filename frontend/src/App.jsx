import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import FAQ from "./pages/FAQ";
import NotFound from "./pages/NotFound";
import AdminDashboard from "./admin/pages/AdminDashboard";
import AboutUs from './pages/AboutUs.jsx';
import Home from './pages/Home.jsx';
import Chat from './pages/Chat.jsx';
import Prediction from './pages/Prediction.jsx';
import Header from './components/Header.jsx';
import Footer from './components/Footer.jsx';

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
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/faq" element={<FAQ />} />
            <Route 
              path="/assessment" 
              element={

                  <Prediction />

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

                  <Chat />

              } 
            />
            <Route 
              path="/admin" 
              element={

                  <AdminDashboard />

              } 
            />
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

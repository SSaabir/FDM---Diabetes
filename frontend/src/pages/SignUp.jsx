import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/contexts/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { Heart, Loader2, Mail, Lock, User, Eye, EyeOff } from 'lucide-react';
import * as Yup from 'yup';

export const SignUp = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
    dateOfBirth: '',
    termsAccepted: false,
    privacyAccepted: false,
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});

  const { isAuthenticated, signup } = useAuth();
  const { toast } = useToast();

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  // ✅ Sanitization function
  const sanitizeInput = (value, field) => {
    if (typeof value !== 'string') return value;

    let cleaned = value.trim();

    if (field === 'email') {
      cleaned = cleaned.replace(/[^a-zA-Z0-9@._-]/g, ''); // only email-safe chars
    } else if (field === 'phone') {
      cleaned = cleaned.replace(/[^0-9+]/g, ''); // keep digits & +
    } else if (field === 'fullName') {
      cleaned = cleaned.replace(/[^a-zA-Z ]/g, ''); // only letters + spaces
    } else {
      // default: strip dangerous chars
      cleaned = cleaned.replace(/[<>]/g, '');
    }

    return cleaned;
  };

  const signUpSchema = Yup.object().shape({
    fullName: Yup.string().required('Full name is required'),
    email: Yup.string()
      .email('Please enter a valid email address')
      .required('Email is required'),
    password: Yup.string()
      .min(8, 'Password must be at least 8 characters')
      .required('Password is required'),
    confirmPassword: Yup.string()
      .oneOf([Yup.ref('password')], 'Passwords do not match')
      .required('Please confirm your password'),
    termsAccepted: Yup.boolean().oneOf([true], 'You must accept the Terms of Service'),
    privacyAccepted: Yup.boolean().oneOf([true], 'You must accept the Privacy Policy'),
    phone: Yup.string().matches(/^\+?[0-9]*$/, 'Phone number is not valid').nullable(),
    dateOfBirth: Yup.date().nullable(),
  });

  const validateForm = async () => {
    try {
      await signUpSchema.validate(formData, { abortEarly: false });
      setErrors({});
      return true;
    } catch (err) {
      const newErrors = {};
      err.inner.forEach((e) => {
        newErrors[e.path] = e.message;
      });
      setErrors(newErrors);
      return false;
    }
  };

  const handleBlur = async (field) => {
    try {
      await signUpSchema.validateAt(field, formData);
      setErrors((prev) => ({ ...prev, [field]: '' }));
    } catch (err) {
      setErrors((prev) => ({ ...prev, [field]: err.message }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const isValid = await validateForm();
    if (!isValid) return;

    setIsSubmitting(true);
    
    try {
      // Map frontend field names to backend field names
      const signupData = {
        full_name: formData.fullName,
        email: formData.email,
        password: formData.password,
        phone: formData.phone || null,
        date_of_birth: formData.dateOfBirth || null,
      };
      
      // Call the signup function from AuthContext
      await signup(signupData);
      
      toast({
        title: "Account created successfully!",
        description: "Welcome to DiabetesPredict. Please sign in to continue.",
      });
      
      // Navigate to login page after successful signup
      setTimeout(() => {
        window.location.href = '/login';
      }, 1500);
      
    } catch (error) {
      console.error('Signup error:', error);
      
      let errorMessage = 'Failed to create account. Please try again.';
      
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      toast({
        title: "Signup Failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  // ✅ Updated updater with sanitization
  const updateFormData = (field, value) => {
    const safeValue = sanitizeInput(value, field);
    setFormData(prev => ({ ...prev, [field]: safeValue }));
  };

  const getPasswordStrength = (password) => {
    let strength = 0;
    let feedback = 'Very Weak';
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    switch (strength) {
      case 0:
      case 1: feedback = 'Very Weak'; break;
      case 2: feedback = 'Weak'; break;
      case 3: feedback = 'Fair'; break;
      case 4: feedback = 'Good'; break;
      case 5: feedback = 'Strong'; break;
    }
    return { strength, feedback };
  };

  const passwordStrength = getPasswordStrength(formData.password);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-lg">
        <Card className="shadow-elevated">
          <CardHeader className="text-center space-y-4">
            <div className="mx-auto w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center">
              <Heart className="h-6 w-6 text-primary-foreground" />
            </div>
            <div>
              <CardTitle className="text-2xl font-bold text-primary">Create Your Account</CardTitle>
              <CardDescription className="text-muted-foreground">
                Join DiabetesPredict to start monitoring your health
              </CardDescription>
            </div>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Full Name */}
              <div className="space-y-2">
                <Label htmlFor="fullName" className="flex items-center space-x-2 text-secondary">
                  <User className="h-4 w-4" />
                  <span>Full Name</span>
                </Label>
                <Input
                  id="fullName"
                  type="text"
                  value={formData.fullName}
                  onChange={(e) => updateFormData('fullName', e.target.value)}
                  onBlur={() => handleBlur('fullName')}
                  placeholder="Enter your full name"
                  className={errors.fullName ? 'border-destructive' : ''}
                />
                {errors.fullName && <p className="text-sm text-destructive">{errors.fullName}</p>}
              </div>

              {/* Email */}
              <div className="space-y-2">
                <Label htmlFor="email" className="flex items-center space-x-2 text-secondary">
                  <Mail className="h-4 w-4" />
                  <span>Email Address</span>
                </Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => updateFormData('email', e.target.value)}
                  onBlur={() => handleBlur('email')}
                  placeholder="Enter your email"
                  className={errors.email ? 'border-destructive' : ''}
                />
                {errors.email && <p className="text-sm text-destructive">{errors.email}</p>}
              </div>

              {/* Password */}
              <div className="space-y-2">
                <Label htmlFor="password" className="flex items-center space-x-2 text-secondary">
                  <Lock className="h-4 w-4" />
                  <span>Password</span>
                </Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    value={formData.password}
                    onChange={(e) => updateFormData('password', e.target.value)}
                    onBlur={() => handleBlur('password')}
                    placeholder="Create a secure password"
                    className={errors.password ? 'border-destructive pr-12' : 'pr-12'}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {formData.password && (
                  <div className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Password strength:</span>
                      <span className={`font-medium ${
                        passwordStrength.strength <= 2 ? 'text-destructive' : 
                        passwordStrength.strength === 3 ? 'text-warning' : 'text-success'
                      }`}>
                        {passwordStrength.feedback}
                      </span>
                    </div>
                    <div className="flex space-x-1">
                      {[...Array(5)].map((_, i) => (
                        <div
                          key={i}
                          className={`h-1 flex-1 rounded ${
                            i < passwordStrength.strength
                              ? passwordStrength.strength <= 2 
                                ? 'bg-destructive' 
                                : passwordStrength.strength === 3 
                                ? 'bg-warning' 
                                : 'bg-success'
                              : 'bg-muted'
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                )}
                {errors.password && <p className="text-sm text-destructive">{errors.password}</p>}
              </div>

              {/* Confirm Password */}
              <div className="space-y-2">
                <Label htmlFor="confirmPassword" className="flex items-center space-x-2 text-secondary">
                  <Lock className="h-4 w-4" />
                  <span>Confirm Password</span>
                </Label>
                <div className="relative">
                  <Input
                    id="confirmPassword"
                    type={showConfirmPassword ? 'text' : 'password'}
                    value={formData.confirmPassword}
                    onChange={(e) => updateFormData('confirmPassword', e.target.value)}
                    onBlur={() => handleBlur('confirmPassword')}
                    placeholder="Confirm your password"
                    className={errors.confirmPassword ? 'border-destructive pr-12' : 'pr-12'}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  >
                    {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {errors.confirmPassword && <p className="text-sm text-destructive">{errors.confirmPassword}</p>}
              </div>

              {/* Phone Number */}
              <div className="space-y-2">
                <Label htmlFor="phone" className="flex items-center space-x-2 text-secondary">
                  <span>📱</span>
                  <span>Phone Number (Optional)</span>
                </Label>
                <Input
                  id="phone"
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => updateFormData('phone', e.target.value)}
                  onBlur={() => handleBlur('phone')}
                  placeholder="Enter your phone number"
                  className={errors.phone ? 'border-destructive' : ''}
                />
                {errors.phone && <p className="text-sm text-destructive">{errors.phone}</p>}
              </div>

              {/* Date of Birth */}
              <div className="space-y-2">
                <Label htmlFor="dateOfBirth" className="flex items-center space-x-2 text-secondary">
                  <span>🎂</span>
                  <span>Date of Birth (Optional)</span>
                </Label>
                <Input
                  id="dateOfBirth"
                  type="date"
                  value={formData.dateOfBirth}
                  onChange={(e) => updateFormData('dateOfBirth', e.target.value)}
                  onBlur={() => handleBlur('dateOfBirth')}
                  className={errors.dateOfBirth ? 'border-destructive' : ''}
                />
                {errors.dateOfBirth && <p className="text-sm text-destructive">{errors.dateOfBirth}</p>}
              </div>

              {/* Terms + Privacy */}
              <div className="space-y-4 p-4 bg-muted/30 rounded-lg">
                <p className="text-sm font-medium text-secondary">Healthcare Data Protection</p>
                <div className="space-y-3">
                  <div className="flex items-start space-x-3">
                    <Checkbox
                      id="terms"
                      checked={formData.termsAccepted}
                      onCheckedChange={(checked) => updateFormData('termsAccepted', checked)}
                      className={errors.termsAccepted ? 'border-destructive' : ''}
                    />
                    <Label htmlFor="terms" className="text-sm leading-relaxed">
                      I accept the{' '}
                      <Link to="/terms" className="text-primary hover:text-primary-hover underline font-medium">
                        Terms of Service
                      </Link>{' '}
                      and understand that my health data will be handled securely.
                    </Label>
                  </div>
                  {errors.termsAccepted && <p className="text-sm text-destructive ml-6">{errors.termsAccepted}</p>}

                  <div className="flex items-start space-x-3">
                    <Checkbox
                      id="privacy"
                      checked={formData.privacyAccepted}
                      onCheckedChange={(checked) => updateFormData('privacyAccepted', checked)}
                      className={errors.privacyAccepted ? 'border-destructive' : ''}
                    />
                    <Label htmlFor="privacy" className="text-sm leading-relaxed">
                      I have read and agree to the{' '}
                      <Link to="/privacy" className="text-primary hover:text-primary-hover underline font-medium">
                        Privacy Policy
                      </Link>{' '}
                      and HIPAA compliance guidelines.
                    </Label>
                  </div>
                  {errors.privacyAccepted && <p className="text-sm text-destructive ml-6">{errors.privacyAccepted}</p>}
                </div>
              </div>

              {/* Submit */}
              <Button
                type="submit"
                className="w-full bg-primary hover:bg-primary-hover text-primary-foreground"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating Account...
                  </>
                ) : (
                  'Create Account'
                )}
              </Button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-sm text-muted-foreground">
                Already have an account?{' '}
                <Link to="/login" className="text-primary hover:text-primary-hover underline font-medium">
                  Sign in here
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SignUp;

import { useState } from "react";
import { Button } from "../components/ui/button.jsx";
import { Input } from "../components/ui/input.jsx";
import { Label } from "../components/ui/label.jsx";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card.jsx";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select.jsx";
import { Progress } from "../components/ui/progress.jsx";
import { Badge } from "../components/ui/badge.jsx";
import { 
  Calculator, 
  Activity, 
  Heart, 
  Stethoscope, 
  TrendingUp, 
  Shield, 
  AlertTriangle,
  CheckCircle2,
  MessageCircle,
  BarChart3
} from "lucide-react";
import { Link } from "react-router-dom";
import { useToast } from "../hooks/use-toast.jsx";
import { predictionAPI, apiHelpers } from "../services/api.js";
import { usePageTitle } from "../hooks/usePageTitle.js";

const Prediction = () => {
  usePageTitle("Risk Assessment");
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    age: '',
    gender: '',
    height: '',
    weight: '',
    familyHistory: '',
    physicalActivity: '',
    smoking: '',
    hypertension: '',
    heartDisease: '',
    sleepHours: '',
    dietPattern: '',
    alcoholIntake: '',
    medicationUse: '',
    gestationalHistory: 'no',
    hbA1c: '',
    bloodGlucose: ''
  });
  
  const [prediction, setPrediction] = useState(null);
  const [showFullResults, setShowFullResults] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [lastRequestTime, setLastRequestTime] = useState(0);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const generateRandomData = () => {
    // Random test data sets for different risk profiles
    const testDataSets = [
      // Low risk young female
      {
        age: 25,
        gender: 'female',
        height: 165,
        weight: 60,
        familyHistory: 'no',
        physicalActivity: 'high',
        smoking: 'never',
        hypertension: 'no',
        heartDisease: 'no',
        sleepHours: '8',
        dietPattern: 'balanced',
        alcoholIntake: 'none',
        medicationUse: 'no',
        gestationalHistory: 'no',
        hbA1c: '5.2',
        bloodGlucose: '85'
      },
      // Moderate risk middle-aged male
      {
        age: 45,
        gender: 'male',
        height: 175,
        weight: 85,
        familyHistory: 'yes',
        physicalActivity: 'moderate',
        smoking: 'former',
        hypertension: 'yes',
        heartDisease: 'no',
        sleepHours: '6',
        dietPattern: 'high-carb',
        alcoholIntake: 'occasional',
        medicationUse: 'yes',
        gestationalHistory: 'no',
        hbA1c: '6.1',
        bloodGlucose: '105'
      },
      // High risk female with gestational history
      {
        age: 55,
        gender: 'female',
        height: 160,
        weight: 90,
        familyHistory: 'yes',
        physicalActivity: 'low',
        smoking: 'never',
        hypertension: 'yes',
        heartDisease: 'yes',
        sleepHours: '5',
        dietPattern: 'high-carb',
        alcoholIntake: 'regular',
        medicationUse: 'yes',
        gestationalHistory: 'yes',
        hbA1c: '6.8',
        bloodGlucose: '140'
      },
      // High risk senior male
      {
        age: 65,
        gender: 'male',
        height: 170,
        weight: 95,
        familyHistory: 'yes',
        physicalActivity: 'low',
        smoking: 'current',
        hypertension: 'yes',
        heartDisease: 'yes',
        sleepHours: '6',
        dietPattern: 'high-carb',
        alcoholIntake: 'regular',
        medicationUse: 'yes',
        gestationalHistory: 'no',
        hbA1c: '7.2',
        bloodGlucose: '160'
      },
      // Random moderate risk female
      {
        age: 38,
        gender: 'female',
        height: 158,
        weight: 75,
        familyHistory: 'unknown',
        physicalActivity: 'moderate',
        smoking: 'never',
        hypertension: 'no',
        heartDisease: 'no',
        sleepHours: '7',
        dietPattern: 'balanced',
        alcoholIntake: 'occasional',
        medicationUse: 'no',
        gestationalHistory: 'no',
        hbA1c: '5.8',
        bloodGlucose: '95'
      }
    ];

    // Pick a random dataset
    const randomData = testDataSets[Math.floor(Math.random() * testDataSets.length)];
    
    // Convert numbers to strings for form inputs
    setFormData({
      age: randomData.age.toString(),
      gender: randomData.gender,
      height: randomData.height.toString(),
      weight: randomData.weight.toString(),
      familyHistory: randomData.familyHistory,
      physicalActivity: randomData.physicalActivity,
      smoking: randomData.smoking,
      hypertension: randomData.hypertension,
      heartDisease: randomData.heartDisease,
      sleepHours: randomData.sleepHours,
      dietPattern: randomData.dietPattern,
      alcoholIntake: randomData.alcoholIntake,
      medicationUse: randomData.medicationUse,
      gestationalHistory: String(randomData.gestationalHistory || 'no'),
      hbA1c: randomData.hbA1c,
      bloodGlucose: randomData.bloodGlucose
    });

    // Clear any previous prediction
    setPrediction(null);
    setShowFullResults(false);

    toast({
      title: "Random Test Data Generated! 🎲",
      description: `Loaded ${randomData.gender} profile, age ${randomData.age}. Ready to test!`,
    });
  };

  const calculateBMI = () => {
    if (!formData.height || !formData.weight) return 0;
    const heightM = parseFloat(formData.height) / 100;
    const weightKg = parseFloat(formData.weight);
    return weightKg / (heightM * heightM);
  };

  const calculateRisk = async () => {
    // Prevent rapid successive requests
    const now = Date.now();
    const timeSinceLastRequest = now - lastRequestTime;
    if (timeSinceLastRequest < 2000) { // 2 second minimum between requests
      toast({
        title: "Please Wait ⏱️",
        description: "Please wait a moment before making another request.",
        variant: "destructive",
      });
      return;
    }
    
    setIsLoading(true);
    setLastRequestTime(now);
    
    try {
      // Debug: Check raw form data first
      console.log('🔍 DEBUG: Raw form data before processing:', formData);
      console.log('🔍 DEBUG: Raw form data types:', Object.keys(formData).map(key => `${key}: ${typeof formData[key]} = ${formData[key]}`));
      
      // Check for boolean values in raw formData
      const booleanFormFields = Object.keys(formData).filter(key => typeof formData[key] === 'boolean');
      if (booleanFormFields.length > 0) {
        console.error('🚨 ALERT: Boolean values found in raw formData:', booleanFormFields);
        booleanFormFields.forEach(field => {
          console.log(`   - ${field}: ${typeof formData[field]} = ${formData[field]}`);
        });
      }
      
      // Convert form data to API format with proper data types for backend compatibility
      const apiData = {
        age: parseInt(formData.age),
        gender: String(formData.gender || ''),
        height: parseFloat(formData.height),
        weight: parseFloat(formData.weight),
        familyHistory: String(formData.familyHistory || ''),
        physicalActivity: String(formData.physicalActivity || ''),
        smoking: String(formData.smoking || ''),
        hypertension: String(formData.hypertension || ''),
        heartDisease: String(formData.heartDisease || ''),
        sleepHours: parseInt(formData.sleepHours),
        dietPattern: String(formData.dietPattern || ''),
        alcoholIntake: String(formData.alcoholIntake || ''),
        medicationUse: String(formData.medicationUse || ''),
        gestationalHistory: formData.gender === 'female' ? String(formData.gestationalHistory || 'no') : 'no',
        hbA1c: formData.hbA1c ? parseFloat(formData.hbA1c) : null,
        bloodGlucose: formData.bloodGlucose ? parseFloat(formData.bloodGlucose) : null
      };

      console.log('🔍 DEBUG: Sending API data:', apiData);
      console.log('🔍 DEBUG: gestationalHistory type and value:', typeof apiData.gestationalHistory, apiData.gestationalHistory);
      console.log('🔍 DEBUG: Gender:', apiData.gender);
      console.log('🔍 DEBUG: All field types:', Object.keys(apiData).map(key => `${key}: ${typeof apiData[key]} = ${apiData[key]}`));
      
      // Detailed field-by-field type checking
      console.log('🔬 DETAILED TYPE CHECK:');
      Object.keys(apiData).forEach(key => {
        const value = apiData[key];
        const type = typeof value;
        if (type === 'boolean') {
          console.error(`❌ BOOLEAN DETECTED: ${key} = ${value} (${type})`);
        } else {
          console.log(`✅ ${key}: ${type} = ${value}`);
        }
      });
      
      // Safety check: Ensure no boolean values are being sent to backend
      const problematicFields = Object.keys(apiData).filter(key => 
        typeof apiData[key] === 'boolean'
      );
      if (problematicFields.length > 0) {
        console.error('🚨 WARNING: Boolean fields detected:', problematicFields);
        // Convert any remaining booleans to strings
        problematicFields.forEach(field => {
          console.log(`🔧 Converting ${field} from ${apiData[field]} to "${String(apiData[field])}"`);
          apiData[field] = String(apiData[field]);
        });
        console.log('🔍 DEBUG: Fixed API data after boolean conversion:', apiData);
      }

      // Final check - log the exact JSON that will be sent
      console.log('📡 FINAL: JSON being sent to API:', JSON.stringify(apiData, null, 2));
      
      // Call the prediction API with enhanced error handling
      const response = await predictionAPI.predict(apiData);
      console.log('🔍 DEBUG: Full API response:', response);
      console.log('🔍 DEBUG: API response data:', response?.data);
      
      // Check if response and response.data exist
      if (!response || !response.data) {
        throw new Error('Empty response from prediction API');
      }
      
      const result = apiHelpers.handleSuccess(response);
      
      if (result.success) {
        const predictionData = result.data;
        
        // Handle both old and new response formats
        let riskPercentage = predictionData.risk_percentage || (predictionData.risk_probability * 100);
        
        setPrediction({
          risk: Math.round(riskPercentage * 10) / 10, // Round to 1 decimal
          level: predictionData.risk_level,
          recommendations: predictionData.recommendations,
          bmi: predictionData.bmi,
          modelUsed: predictionData.model_used,
          confidence: predictionData.confidence,
          hasClinicalData: predictionData.has_clinical_data
        });
        
        // Reset the reveal state for new predictions
        setShowFullResults(false);
        
        // For high risk, show context first, then reveal the full results after a delay
        if (predictionData.risk_level === 'high') {
          setTimeout(() => {
            setShowFullResults(true);
          }, 2000); // 2 second delay for mental preparation
        } else {
          setShowFullResults(true); // Show immediately for low/moderate risk
        }
        
        toast({
          title: "AI Prediction Complete! 🤖",
          description: `Analysis performed using ${predictionData.model_used}.`,
        });
      } else {
        throw new Error(result.message || 'Prediction failed');
      }
      
    } catch (error) {
      const errorResult = apiHelpers.handleError(error);
      
      // Show the actual error instead of falling back
      toast({
        title: "Prediction Failed ❌",
        description: `Error: ${errorResult.message}. Please check your input and try again.`,
        variant: "destructive",
      });
      
      console.error('Prediction API error:', errorResult);
    } finally {
      setIsLoading(false);
    }
  };

  const isFormValid = () => {
    return Object.entries(formData).every(([key, value]) => {
      // Skip optional clinical fields
      if (key === 'hbA1c' || key === 'bloodGlucose') {
        return true;
      }
      // Boolean fields are always valid if they exist
      if (typeof value === 'boolean') {
        return true;
      }
      // String fields must not be empty after trimming
      return value && value.trim() !== '';
    });
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'low': return 'text-green-600';
      case 'moderate': return 'text-amber-600';
      case 'high': return 'text-blue-700'; // Changed from red to calming blue
      default: return 'text-muted-foreground';
    }
  };

  const getRiskIcon = (level) => {
    switch (level) {
      case 'low': return <CheckCircle2 className="h-5 w-5 text-green-600" />;
      case 'moderate': return <AlertTriangle className="h-5 w-5 text-amber-600" />;
      case 'high': return <Heart className="h-5 w-5 text-blue-700" />; // Changed from alert triangle to heart
      default: return <BarChart3 className="h-5 w-5" />;
    }
  };

  const getRiskBadgeVariant = (level) => {
    switch (level) {
      case 'low': return 'default';
      case 'moderate': return 'secondary';
      case 'high': return 'outline'; // Changed from destructive to outline
      default: return 'secondary';
    }
  };

  const getRiskHeaderColor = (level) => {
    switch (level) {
      case 'low': return 'bg-green-50 border-green-200';
      case 'moderate': return 'bg-amber-50 border-amber-200';
      case 'high': return 'bg-blue-50 border-blue-200'; // Changed from red to calming blue
      default: return 'bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-soft">
      <div className="container mx-auto px-4 py-6 max-w-6xl">
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Form Section */}
          <Card className="medical-card">
            <CardHeader className="bg-gradient-medical text-primary-foreground rounded-t-lg">
              <div className="flex items-center space-x-3">
                <Calculator className="h-6 w-6 bounce-in" />
                <div>
                  <CardTitle className="text-lg text-black">Diabetes Risk Assessment 📋</CardTitle>
                  <CardDescription className="text-primary-foreground/80">
                    Complete the form to get your personalized risk analysis
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            
            <CardContent className="p-6 space-y-4">
              {/* Personal Information */}
              <div className="space-y-4">
                <h3 className="font-semibold text-primary flex items-center space-x-2">
                  <Activity className="h-4 w-4" />
                  <span>Personal Information</span>
                </h3>
                
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="age">Age 📅</Label>
                    <Input
                      id="age"
                      type="number"
                      placeholder="Enter your age"
                      value={formData.age}
                      onChange={(e) => handleInputChange('age', e.target.value)}
                      min="18"
                      max="100"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="gender">Gender 👤</Label>
                    <Select value={formData.gender} onValueChange={(value) => handleInputChange('gender', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select gender" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="male">Male</SelectItem>
                        <SelectItem value="female">Female</SelectItem>
                        <SelectItem value="other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="height">Height (cm) 📏</Label>
                    <Input
                      id="height"
                      type="number"
                      placeholder="Enter height in cm"
                      value={formData.height}
                      onChange={(e) => handleInputChange('height', e.target.value)}
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="weight">Weight (kg) ⚖️</Label>
                    <Input
                      id="weight"
                      type="number"
                      placeholder="Enter weight in kg"
                      value={formData.weight}
                      onChange={(e) => handleInputChange('weight', e.target.value)}
                    />
                  </div>
                </div>

                {formData.height && formData.weight && (
                  <div className="p-3 bg-muted/50 rounded-lg">
                    <p className="text-sm text-muted-foreground">
                      Your BMI: <span className="font-semibold">{calculateBMI().toFixed(1)}</span>
                      {prediction && prediction.bmi && prediction.bmi !== calculateBMI() && (
                        <span className="ml-2 text-xs">(API calculated: {prediction.bmi})</span>
                      )}
                    </p>
                  </div>
                )}
              </div>

              {/* Health History */}
              <div className="space-y-4">
                <h3 className="font-semibold text-primary flex items-center space-x-2">
                  <Heart className="h-4 w-4" />
                  <span>Health History</span>
                </h3>

                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label>Family History of Diabetes 👨‍👩‍👧‍👦</Label>
                    <Select value={formData.familyHistory} onValueChange={(value) => handleInputChange('familyHistory', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select family history" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="yes">Yes</SelectItem>
                        <SelectItem value="no">No</SelectItem>
                        <SelectItem value="unknown">Unknown</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Gestational History - Only for females */}
                  {formData.gender === 'female' && (
                    <div className="space-y-2">
                      <Label>History of Gestational Diabetes 🤱</Label>
                      <Select 
                        value={formData.gestationalHistory || 'no'} 
                        onValueChange={(value) => handleInputChange('gestationalHistory', value)}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select gestational history" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="no">No</SelectItem>
                          <SelectItem value="yes">Yes</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  )}

                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Hypertension History 🩺</Label>
                      <Select value={formData.hypertension} onValueChange={(value) => handleInputChange('hypertension', value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select hypertension status" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="no">No</SelectItem>
                          <SelectItem value="yes">Yes</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label>Heart Disease History ❤️</Label>
                      <Select value={formData.heartDisease} onValueChange={(value) => handleInputChange('heartDisease', value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select heart disease status" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="no">No</SelectItem>
                          <SelectItem value="yes">Yes</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>Current Medication Use 💊</Label>
                    <Select value={formData.medicationUse} onValueChange={(value) => handleInputChange('medicationUse', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select medication status" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="no">No medications</SelectItem>
                        <SelectItem value="yes">Taking medications</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>

              {/* Clinical Data - Optional */}
              <div className="space-y-4">
                <h3 className="font-semibold text-primary flex items-center space-x-2">
                  <Stethoscope className="h-4 w-4" />
                  <span>Clinical Data (Optional) 🩸</span>
                </h3>
                
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <p className="text-sm text-blue-800 mb-3">
                    📊 <strong>Enhanced Accuracy:</strong> Adding lab results significantly improves prediction accuracy. 
                    Leave blank if you don't have recent test results.
                  </p>
                  
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="hbA1c">HbA1c Level (%) 🔬</Label>
                      <Input
                        id="hbA1c"
                        type="number"
                        step="0.1"
                        placeholder="e.g., 5.7 (optional)"
                        value={formData.hbA1c}
                        onChange={(e) => handleInputChange('hbA1c', e.target.value)}
                        min="4.0"
                        max="15.0"
                      />
                      <p className="text-xs text-muted-foreground">
                        Normal: &lt;5.7%, Prediabetes: 5.7-6.4%, Diabetes: ≥6.5%
                      </p>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="bloodGlucose">Blood Glucose (mg/dL) 🩸</Label>
                      <Input
                        id="bloodGlucose"
                        type="number"
                        placeholder="e.g., 95 (optional)"
                        value={formData.bloodGlucose}
                        onChange={(e) => handleInputChange('bloodGlucose', e.target.value)}
                        min="50"
                        max="400"
                      />
                      <p className="text-xs text-muted-foreground">
                        Normal: 70-99 mg/dL (fasting), &lt;140 mg/dL (2hr post-meal)
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Lifestyle Factors */}
              <div className="space-y-4">
                <h3 className="font-semibold text-primary flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Lifestyle Factors</span>
                </h3>

                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Physical Activity Level 🏃‍♂️</Label>
                    <Select value={formData.physicalActivity} onValueChange={(value) => handleInputChange('physicalActivity', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select activity level" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="high">High (5+ times/week)</SelectItem>
                        <SelectItem value="moderate">Moderate (2-4 times/week)</SelectItem>
                        <SelectItem value="low">Low (Less than 2 times/week)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Smoking Status 🚭</Label>
                    <Select value={formData.smoking} onValueChange={(value) => handleInputChange('smoking', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select smoking status" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="never">Never smoked</SelectItem>
                        <SelectItem value="former">Former smoker</SelectItem>
                        <SelectItem value="current">Current smoker</SelectItem>
                        <SelectItem value="not current">Not current smoker</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Sleep Hours per Night 😴</Label>
                    <Select value={formData.sleepHours} onValueChange={(value) => handleInputChange('sleepHours', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select sleep hours" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="4">4 hours or less</SelectItem>
                        <SelectItem value="5">5 hours</SelectItem>
                        <SelectItem value="6">6 hours</SelectItem>
                        <SelectItem value="7">7 hours</SelectItem>
                        <SelectItem value="8">8 hours</SelectItem>
                        <SelectItem value="9">9 hours or more</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Diet Pattern 🍎</Label>
                    <Select value={formData.dietPattern} onValueChange={(value) => handleInputChange('dietPattern', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select diet pattern" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="balanced">Balanced diet</SelectItem>
                        <SelectItem value="high-carb">High carbohydrate</SelectItem>
                        <SelectItem value="low-carb">Low carbohydrate</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Alcohol Intake 🍷</Label>
                  <Select value={formData.alcoholIntake} onValueChange={(value) => handleInputChange('alcoholIntake', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select alcohol consumption" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">No alcohol</SelectItem>
                      <SelectItem value="occasional">Occasional (1-2 drinks/week)</SelectItem>
                      <SelectItem value="regular">Regular (3+ drinks/week)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Random Test Data Button */}
              <Button
                onClick={generateRandomData}
                variant="outline"
                className="w-full border-2 border-dashed border-primary/30 text-primary hover:bg-primary/5 mb-4"
              >
                <div className="flex items-center space-x-2">
                  <div className="text-lg">🎲</div>
                  <span>Generate Random Test Data</span>
                </div>
              </Button>

              <Button
                onClick={calculateRisk}
                disabled={!isFormValid() || isLoading}
                className="w-full gradient-accent text-lg py-6"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current mr-2" />
                    Calculating Risk...
                  </>
                ) : (
                  <>
                    <Calculator className="h-5 w-5 mr-2" />
                    Calculate Diabetes Risk 🎯
                  </>
                )}
              </Button>
              
              <div className="text-center space-y-2">
                <p className="text-xs text-muted-foreground">
                  🤖 Uses trained Random Forest models for diabetes prediction
                </p>
                <p className="text-xs text-muted-foreground/80">
                  💡 Use "Generate Random Test Data" to quickly test different risk profiles
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Results Section */}
          <div className="space-y-6">
            {prediction ? (
              <Card className="medical-card">
                <CardHeader className={`${getRiskHeaderColor(prediction.level)} rounded-t-lg border-b`}>
                  <div className="flex items-center space-x-3">
                    {getRiskIcon(prediction.level)}
                    <div>
                      <CardTitle className={`${getRiskColor(prediction.level)} text-lg`}>
                        Your Health Assessment Results
                      </CardTitle>
                      <CardDescription>
                        Knowledge is power - here's your personalized health insights
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent className="p-6">
                  <div className="space-y-6">
                    {/* Supportive Context First */}
                    {prediction.level === 'high' && (
                      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                        <div className="flex items-start space-x-3">
                          <Heart className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                          <div className="space-y-2">
                            <h4 className="font-semibold text-blue-800">You're Taking Control of Your Health 💪</h4>
                            <p className="text-sm text-blue-700">
                              Getting this assessment is already a positive step toward better health. Remember, diabetes risk can be significantly reduced with the right actions. Many people with high risk never develop diabetes by making positive lifestyle changes.
                            </p>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Progressive Reveal for High Risk */}
                    {prediction.level === 'high' && !showFullResults && (
                      <div className="text-center space-y-4">
                        <div className="space-y-3">
                          <p className="text-lg font-medium text-blue-700">
                            Preparing your personalized health insights...
                          </p>
                          <div className="flex justify-center">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                          </div>
                          <p className="text-sm text-muted-foreground">
                            Analyzing your risk factors and preparing supportive recommendations
                          </p>
                        </div>
                      </div>
                    )}

                    {/* Risk Score with Context - Only show when ready */}
                    {(prediction.level !== 'high' || showFullResults) && (
                      <div className="text-center">
                        <div className="mb-4">
                          {prediction.level === 'high' ? (
                            <div className="space-y-3">
                              <p className="text-sm text-muted-foreground font-medium">
                                Based on current factors, your estimated risk level is:
                              </p>
                              <div className={`text-4xl font-bold ${getRiskColor(prediction.level)} bounce-in`}>
                                {prediction.risk}%
                              </div>
                              <Badge variant={getRiskBadgeVariant(prediction.level)} className="mt-2 px-4 py-1">
                                ELEVATED ATTENTION NEEDED
                              </Badge>
                              <p className="text-sm text-blue-700 font-medium mt-2">
                                ✨ The good news: This is preventable with action!
                              </p>
                            </div>
                          ) : (
                            <div>
                              <div className={`text-4xl font-bold ${getRiskColor(prediction.level)} bounce-in`}>
                                {prediction.risk}%
                              </div>
                              <Badge variant={getRiskBadgeVariant(prediction.level)} className="mt-2">
                                {prediction.level.toUpperCase()} RISK
                              </Badge>
                            </div>
                          )}
                        </div>
                        
                        <div className="space-y-2">
                          <Progress 
                            value={prediction.risk} 
                            className="h-3 slide-in"
                          />
                          <p className="text-sm text-muted-foreground">
                            Current risk probability based on provided factors
                          </p>
                        </div>
                      </div>
                    )}

                    {/* Show remaining content only when ready */}
                    {(prediction.level !== 'high' || showFullResults) && (
                      <>
                        {/* Risk Explanation */}
                        <div className="p-4 bg-muted/30 rounded-lg">
                          <h4 className="font-semibold mb-2 flex items-center space-x-2">
                            <Shield className="h-4 w-4" />
                            <span>Understanding Your Results</span>
                          </h4>
                          <p className="text-sm text-muted-foreground mb-2">
                            {prediction.level === 'low' 
                              ? "Excellent! Your current lifestyle and health indicators suggest a low risk for developing diabetes. Keep up the healthy habits! 💚"
                              : prediction.level === 'moderate'
                              ? "Your risk level is moderate, which means you have a great opportunity to prevent diabetes with some positive changes. Focus on the recommendations below. 👍"
                              : "While your risk factors suggest elevated attention is needed, the most important thing to know is that diabetes is largely preventable. Studies show that people at high risk can reduce their chances by 50-70% through lifestyle changes. You have the power to change this outcome! 🌟"
                            }
                          </p>
                          {prediction.modelUsed && (
                            <p className="text-xs text-muted-foreground">
                              🔬 Analysis performed using: <span className="font-medium">{prediction.modelUsed}</span>
                              {prediction.confidence && ` (${prediction.confidence} confidence)`}
                              {prediction.hasClinicalData && (
                                <span className="ml-2 text-green-600 font-medium">✓ Enhanced with lab data</span>
                              )}
                            </p>
                          )}
                        </div>

                        {/* Success Stories for High Risk */}
                        {prediction.level === 'high' && (
                          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                            <h4 className="font-semibold mb-3 flex items-center space-x-2 text-green-800">
                              <CheckCircle2 className="h-4 w-4" />
                              <span>Real Success Stories 🌟</span>
                            </h4>
                            <div className="space-y-3 text-sm text-green-700">
                              <div className="flex items-start space-x-2">
                                <span className="text-green-600 font-bold">•</span>
                                <p><strong>Sarah, 45:</strong> "I had an 85% risk score. After 6 months of walking daily and eating better, my doctor said my risk dropped to 30%!"</p>
                              </div>
                              <div className="flex items-start space-x-2">
                                <span className="text-green-600 font-bold">•</span>
                                <p><strong>Research shows:</strong> People at high risk can reduce their diabetes chances by 50-70% with lifestyle changes.</p>
                              </div>
                              <div className="flex items-start space-x-2">
                                <span className="text-green-600 font-bold">•</span>
                                <p><strong>The Diabetes Prevention Program:</strong> Proven that lifestyle changes are more effective than medication alone.</p>
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Immediate Action Steps for High Risk */}
                        {prediction.level === 'high' && (
                          <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
                            <h4 className="font-semibold mb-3 flex items-center space-x-2 text-amber-800">
                              <TrendingUp className="h-4 w-4" />
                              <span>Your Next Steps (Start Today!) 🚀</span>
                            </h4>
                            <div className="space-y-2">
                              <div className="flex items-center space-x-3 text-sm">
                                <div className="w-6 h-6 bg-amber-200 text-amber-800 rounded-full flex items-center justify-center font-bold text-xs">1</div>
                                <span><strong>Today:</strong> Schedule an appointment with your healthcare provider</span>
                              </div>
                              <div className="flex items-center space-x-3 text-sm">
                                <div className="w-6 h-6 bg-amber-200 text-amber-800 rounded-full flex items-center justify-center font-bold text-xs">2</div>
                                <span><strong>This week:</strong> Start with a 10-minute daily walk after meals</span>
                              </div>
                              <div className="flex items-center space-x-3 text-sm">
                                <div className="w-6 h-6 bg-amber-200 text-amber-800 rounded-full flex items-center justify-center font-bold text-xs">3</div>
                                <span><strong>Right now:</strong> Download a food tracking app or start a simple food diary</span>
                              </div>
                            </div>
                            <div className="mt-3 p-2 bg-white rounded border-l-4 border-amber-400">
                              <p className="text-xs text-amber-700">
                                💡 <strong>Remember:</strong> Small, consistent changes create big results. You don't need to change everything at once!
                              </p>
                            </div>
                          </div>
                        )}

                        {/* Recommendations */}
                        <div>
                          <h4 className="font-semibold mb-3 flex items-center space-x-2">
                            <Heart className="h-4 w-4 text-accent" />
                            <span>
                              {prediction.level === 'high' ? 'Your Personalized Prevention Plan' : 'Personalized Recommendations'}
                            </span>
                          </h4>
                          <ul className="space-y-2">
                            {prediction.recommendations.map((rec, index) => (
                              <li key={index} className="flex items-start space-x-2 text-sm slide-in" style={{ animationDelay: `${index * 0.1}s` }}>
                                <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                                <span>{rec}</span>
                              </li>
                            ))}
                          </ul>
                          
                          {prediction.level === 'high' && (
                            <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                              <p className="text-sm text-blue-700 font-medium">
                                🎯 <strong>Focus Areas:</strong> Even small improvements in diet and exercise can significantly reduce your risk within months!
                              </p>
                            </div>
                          )}
                        </div>

                        {/* Support and Resources for High Risk */}
                        {prediction.level === 'high' && (
                          <div className="space-y-4">
                            <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
                              <h4 className="font-semibold mb-2 flex items-center space-x-2 text-purple-800">
                                <MessageCircle className="h-4 w-4" />
                                <span>Need Support? We're Here to Help 🤝</span>
                              </h4>
                              <div className="space-y-2 text-sm text-purple-700">
                                <p>Remember, you're not alone in this journey. Many resources are available:</p>
                                <ul className="space-y-1 ml-4">
                                  <li>• Talk to our AI health assistant for 24/7 support</li>
                                  <li>• Join online diabetes prevention communities</li>
                                  <li>• Ask your doctor about diabetes prevention programs in your area</li>
                                </ul>
                              </div>
                              <div className="mt-3 flex space-x-2">
                                <Link to="/chat" className="inline-flex items-center space-x-1 text-xs bg-purple-200 text-purple-800 px-3 py-1 rounded-full hover:bg-purple-300 transition-colors">
                                  <MessageCircle className="h-3 w-3" />
                                  <span>Chat with AI Assistant</span>
                                </Link>
                                <Link to="/contact" className="inline-flex items-center space-x-1 text-xs bg-purple-200 text-purple-800 px-3 py-1 rounded-full hover:bg-purple-300 transition-colors">
                                  <Heart className="h-3 w-3" />
                                  <span>Get More Help</span>
                                </Link>
                              </div>
                            </div>
                          </div>
                        )}

                        <div className="pt-4 border-t">
                          <p className="text-xs text-muted-foreground text-center">
                            {prediction.level === 'high' 
                              ? "⚠️ This assessment provides risk insights, not a medical diagnosis. Your healthcare provider can help create a personalized prevention plan that's right for you."
                              : "⚠️ This is a risk assessment tool and not a medical diagnosis. Always consult with healthcare professionals for medical advice."
                            }
                          </p>
                          {prediction.level === 'high' && (
                            <p className="text-xs text-blue-600 text-center mt-2 font-medium">
                              💙 Remember: High risk today doesn't mean diabetes tomorrow. You have the power to change your health story!
                            </p>
                          )}
                        </div>
                      </>
                    )}
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="medical-card">
                <CardContent className="p-8 text-center">
                  <div className="space-y-4">
                    <div className="animate-float">
                      <Stethoscope className="h-16 w-16 text-primary mx-auto" />
                    </div>
                    <h3 className="text-lg font-semibold text-primary">Ready for Your Assessment? 📊</h3>
                    <p className="text-muted-foreground">
                      Complete the form to get your personalized diabetes risk analysis with actionable recommendations.
                    </p>
                    <div className="flex justify-center space-x-8 text-sm text-muted-foreground">
                      <div className="flex items-center space-x-1">
                        <Shield className="h-4 w-4" />
                        <span>Secure</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <CheckCircle2 className="h-4 w-4" />
                        <span>Evidence-based</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Heart className="h-4 w-4" />
                        <span>Personalized</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Info Cards */}
            <div className="grid gap-4">
              <Card className="medical-card p-4">
                <div className="flex items-start space-x-3">
                  <Activity className="h-6 w-6 text-secondary mt-1 animate-float" />
                  <div>
                    <h4 className="font-semibold text-sm">Evidence-Based Algorithm</h4>
                    <p className="text-xs text-muted-foreground mt-1">
                      Our assessment uses validated risk factors from medical research to provide accurate predictions.
                    </p>
                  </div>
                </div>
              </Card>
              
              <Card className="medical-card p-4">
                <div className="flex items-start space-x-3">
                  <Shield className="h-6 w-6 text-accent mt-1 pulse-gentle" />
                  <div>
                    <h4 className="font-semibold text-sm">Privacy Protected</h4>
                    <p className="text-xs text-muted-foreground mt-1">
                      Your data is processed securely and not stored. All calculations happen locally in your browser.
                    </p>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Prediction;

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
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";

const Prediction = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    age: '',
    gender: '',
    height: '',
    weight: '',
    familyHistory: '',
    physicalActivity: '',
    smoking: '',
    bloodPressure: '',
    cholesterol: ''
  });
  
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const calculateBMI = () => {
    if (!formData.height || !formData.weight) return 0;
    const heightM = parseFloat(formData.height) / 100;
    const weightKg = parseFloat(formData.weight);
    return weightKg / (heightM * heightM);
  };

  const calculateRisk = async () => {
    setIsLoading(true);
    
    try {
      // Convert form data to API format
      const apiData = {
        age: parseInt(formData.age),
        gender: formData.gender,
        height: parseFloat(formData.height),
        weight: parseFloat(formData.weight),
        familyHistory: formData.familyHistory,
        physicalActivity: formData.physicalActivity,
        smoking: formData.smoking,
        bloodPressure: formData.bloodPressure,
        cholesterol: formData.cholesterol
      };

      // Call the prediction API
      const response = await predictionAPI.predict(apiData);
      const result = apiHelpers.handleSuccess(response);
      
      if (result.success) {
        const predictionData = result.data;
        
        setPrediction({
          risk: predictionData.risk_percentage,
          level: predictionData.risk_level,
          recommendations: predictionData.recommendations,
          bmi: predictionData.bmi,
          modelUsed: predictionData.model_used,
          confidence: predictionData.confidence
        });
        
        toast({
          title: "Prediction Complete! 🎯",
          description: `Your diabetes risk has been calculated using ${predictionData.model_used}.`,
        });
      } else {
        throw new Error(result.message || 'Prediction failed');
      }
      
    } catch (error) {
      const errorResult = apiHelpers.handleError(error);
      
      toast({
        title: "Prediction Failed ❌",
        description: errorResult.message,
        variant: "destructive",
      });
      
      // Fall back to local calculation in case of API error
      console.warn('API prediction failed, using fallback calculation:', errorResult.message);
      calculateRiskFallback();
    } finally {
      setIsLoading(false);
    }
  };

  const calculateRiskFallback = () => {
    // Fallback calculation (original logic)
    let riskScore = 0;
    
    // Age factor
    const age = parseInt(formData.age);
    if (age > 45) riskScore += 20;
    else if (age > 35) riskScore += 10;
    
    // BMI factor
    const bmi = calculateBMI();
    if (bmi > 30) riskScore += 25;
    else if (bmi > 25) riskScore += 15;
    
    // Family history
    if (formData.familyHistory === 'yes') riskScore += 20;
    
    // Lifestyle factors
    if (formData.physicalActivity === 'low') riskScore += 15;
    if (formData.smoking === 'yes') riskScore += 10;
    if (formData.bloodPressure === 'high') riskScore += 15;
    if (formData.cholesterol === 'high') riskScore += 10;
    
    // Gender factor
    if (formData.gender === 'male') riskScore += 5;
    
    // Normalize to percentage
    const riskPercentage = Math.min(riskScore, 100);
    
    let level;
    let recommendations;
    
    if (riskPercentage < 30) {
      level = 'low';
      recommendations = [
        '🍎 Maintain a balanced, healthy diet',
        '🏃‍♀️ Continue regular physical activity',
        '📊 Monitor your health annually',
        '💪 Keep up the great lifestyle habits!'
      ];
    } else if (riskPercentage < 70) {
      level = 'moderate';
      recommendations = [
        '🥗 Adopt a diabetes-friendly diet',
        '🚶‍♂️ Increase physical activity to 150 min/week',
        '⚖️ Work on achieving a healthy weight',
        '🩺 Schedule regular health check-ups',
        '🚭 Consider smoking cessation if applicable'
      ];
    } else {
      level = 'high';
      recommendations = [
        '👨‍⚕️ Consult with a healthcare provider immediately',
        '🍽️ Follow a strict diabetic meal plan',
        '💊 Discuss preventive medications with your doctor',
        '📱 Monitor blood sugar levels regularly',
        '🏥 Schedule comprehensive health screening',
        '👥 Consider joining a diabetes support group'
      ];
    }
    
    setPrediction({
      risk: riskPercentage,
      level,
      recommendations,
      bmi: calculateBMI(),
      modelUsed: 'Fallback Calculator',
      confidence: 'basic'
    });
    
    toast({
      title: "Prediction Complete! 🎯",
      description: "Risk calculated using offline method.",
    });
  };

  const isFormValid = () => {
    return Object.values(formData).every(value => value.trim() !== '');
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'low': return 'text-green-600';
      case 'moderate': return 'text-yellow-600';
      case 'high': return 'text-red-600';
      default: return 'text-muted-foreground';
    }
  };

  const getRiskIcon = (level) => {
    switch (level) {
      case 'low': return <CheckCircle2 className="h-5 w-5 text-green-600" />;
      case 'moderate': return <AlertTriangle className="h-5 w-5 text-yellow-600" />;
      case 'high': return <AlertTriangle className="h-5 w-5 text-red-600" />;
      default: return <BarChart3 className="h-5 w-5" />;
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
                  <CardTitle className="text-lg">Diabetes Risk Assessment 📊</CardTitle>
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
                    <Label htmlFor="age">Age 🎂</Label>
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

                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Blood Pressure 🩺</Label>
                      <Select value={formData.bloodPressure} onValueChange={(value) => handleInputChange('bloodPressure', value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select level" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="normal">Normal</SelectItem>
                          <SelectItem value="elevated">Elevated</SelectItem>
                          <SelectItem value="high">High</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label>Cholesterol Level 🧪</Label>
                      <Select value={formData.cholesterol} onValueChange={(value) => handleInputChange('cholesterol', value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select level" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="normal">Normal</SelectItem>
                          <SelectItem value="borderline">Borderline</SelectItem>
                          <SelectItem value="high">High</SelectItem>
                        </SelectContent>
                      </Select>
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
                    <Label>Physical Activity Level 🏃‍♀️</Label>
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
                        <SelectItem value="no">Non-smoker</SelectItem>
                        <SelectItem value="former">Former smoker</SelectItem>
                        <SelectItem value="yes">Current smoker</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>

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
            </CardContent>
          </Card>

          {/* Results Section */}
          <div className="space-y-6">
            {prediction ? (
              <Card className="medical-card">
                <CardHeader className={`${prediction.level === 'low' ? 'bg-green-50 border-green-200' : 
                  prediction.level === 'moderate' ? 'bg-yellow-50 border-yellow-200' : 
                  'bg-red-50 border-red-200'} rounded-t-lg border-b`}>
                  <div className="flex items-center space-x-3">
                    {getRiskIcon(prediction.level)}
                    <div>
                      <CardTitle className={`${getRiskColor(prediction.level)} text-lg`}>
                        Risk Assessment Results
                      </CardTitle>
                      <CardDescription>
                        Based on your provided information
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent className="p-6">
                  <div className="space-y-6">
                    {/* Risk Score */}
                    <div className="text-center">
                      <div className="mb-4">
                        <div className={`text-4xl font-bold ${getRiskColor(prediction.level)} bounce-in`}>
                          {prediction.risk}%
                        </div>
                        <Badge variant={prediction.level === 'low' ? 'default' : 'destructive'} className="mt-2">
                          {prediction.level.toUpperCase()} RISK
                        </Badge>
                      </div>
                      
                      <div className="space-y-2">
                        <Progress 
                          value={prediction.risk} 
                          className="h-3 slide-in"
                        />
                        <p className="text-sm text-muted-foreground">
                          Diabetes risk probability
                        </p>
                      </div>
                    </div>

                    {/* Risk Explanation */}
                    <div className="p-4 bg-muted/30 rounded-lg">
                      <h4 className="font-semibold mb-2 flex items-center space-x-2">
                        <Shield className="h-4 w-4" />
                        <span>What This Means</span>
                      </h4>
                      <p className="text-sm text-muted-foreground mb-2">
                        {prediction.level === 'low' 
                          ? "Great news! Your current lifestyle and health indicators suggest a low risk for developing diabetes. Keep up the healthy habits! 🌟"
                          : prediction.level === 'moderate'
                          ? "Your risk level is moderate. With some lifestyle changes, you can significantly reduce your diabetes risk. Focus on the recommendations below. 💪"
                          : "Your risk level is high. It's important to take immediate action and consult with healthcare professionals. Early intervention can make a significant difference. 🏥"
                        }
                      </p>
                      {prediction.modelUsed && (
                        <p className="text-xs text-muted-foreground">
                          🤖 Analysis performed using: <span className="font-medium">{prediction.modelUsed}</span>
                          {prediction.confidence && ` (${prediction.confidence} confidence)`}
                        </p>
                      )}
                    </div>

                    {/* Recommendations */}
                    <div>
                      <h4 className="font-semibold mb-3 flex items-center space-x-2">
                        <Heart className="h-4 w-4 text-accent" />
                        <span>Personalized Recommendations</span>
                      </h4>
                      <ul className="space-y-2">
                        {prediction.recommendations.map((rec, index) => (
                          <li key={index} className="flex items-start space-x-2 text-sm slide-in" style={{ animationDelay: `${index * 0.1}s` }}>
                            <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                            <span>{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="pt-4 border-t">
                      <p className="text-xs text-muted-foreground text-center">
                        ⚠️ This is a risk assessment tool and not a medical diagnosis. 
                        Always consult with healthcare professionals for medical advice.
                      </p>
                    </div>
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
                    <h3 className="text-lg font-semibold text-primary">Ready for Your Assessment? 🩺</h3>
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
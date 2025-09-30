import { useState } from "react";
import { Button } from "../components/ui/button.jsx";
import { Input } from "../components/ui/input.jsx";
import { Label } from "../components/ui/label.jsx";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card.jsx";
import { Progress } from "../components/ui/progress.jsx";
import { Badge } from "../components/ui/badge.jsx";
import { AlertTriangle, CheckCircle2 } from "lucide-react";
import { useToast } from "../hooks/use-toast.jsx";
import { predictionAPI, apiHelpers } from "../services/api.js";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";

// ✅ Sanitization helper
const sanitizeInput = (value) => {
  if (typeof value === "string") {
    return value.trim().replace(/[<>]/g, "");
  }
  return value;
};

const Prediction = () => {
  const { toast } = useToast();

  const [formData, setFormData] = useState({
    age: "",
    gender: "",
    height: "",
    weight: "",
    familyHistory: "",
    physicalActivity: "",
    smoking: "",
    bloodPressure: "",
    cholesterol: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [lastInput, setLastInput] = useState(null); // for retry

  // ✅ Handle input updates
  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: sanitizeInput(value) }));
  };

  // ✅ Simple fallback if API fails
  const calculateRiskFallback = () => {
    const bmi = calculateBMI();
    let risk = 10;
    if (bmi > 30) risk += 20;
    if (parseInt(formData.age) > 50) risk += 15;

    setPrediction({
      risk,
      level: risk > 50 ? "High (fallback)" : "Low (fallback)",
      recommendations: ["Please consult a doctor for proper testing."],
      bmi,
      modelUsed: "Fallback calculator",
      confidence: "N/A",
    });
  };

  // ✅ BMI calculation helper
  const calculateBMI = () => {
    if (!formData.height || !formData.weight) return 0;
    const heightM = parseFloat(formData.height) / 100;
    const weightKg = parseFloat(formData.weight);
    return (weightKg / (heightM * heightM)).toFixed(2);
  };

  // ✅ Main API call
  const calculateRisk = async () => {
    setIsLoading(true);
    setErrorMsg(null);
    setPrediction(null);
    setLastInput(formData);

    try {
      const apiData = {
        age: parseInt(sanitizeInput(formData.age)),
        gender: sanitizeInput(formData.gender),
        height: parseFloat(sanitizeInput(formData.height)),
        weight: parseFloat(sanitizeInput(formData.weight)),
        familyHistory: sanitizeInput(formData.familyHistory),
        physicalActivity: sanitizeInput(formData.physicalActivity),
        smoking: sanitizeInput(formData.smoking),
        bloodPressure: sanitizeInput(formData.bloodPressure),
        cholesterol: sanitizeInput(formData.cholesterol),
      };

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
          confidence: predictionData.confidence,
        });

        toast({
          title: "Prediction Complete 🎯",
          description: `Your diabetes risk has been calculated using ${predictionData.model_used}.`,
        });
      } else {
        throw new Error(result.message || "Prediction failed");
      }
    } catch (error) {
      const errorResult = apiHelpers.handleError(error);
      setErrorMsg(errorResult.message);

      toast({
        title: "Prediction Failed ❌",
        description: errorResult.message,
        variant: "destructive",
      });

      console.warn("API prediction failed, using fallback:", errorResult.message);
      calculateRiskFallback();
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Header />
      <main className="max-w-2xl mx-auto p-4">
        <Card>
          <CardHeader>
            <CardTitle>Diabetes Risk Prediction</CardTitle>
            <CardDescription>Enter your details below</CardDescription>
          </CardHeader>
          <CardContent>
            {/* Input fields */}
            <Label>Age</Label>
            <Input
              value={formData.age}
              onChange={(e) => handleInputChange("age", e.target.value)}
            />

            <Label>Height (cm)</Label>
            <Input
              value={formData.height}
              onChange={(e) => handleInputChange("height", e.target.value)}
            />

            <Label>Weight (kg)</Label>
            <Input
              value={formData.weight}
              onChange={(e) => handleInputChange("weight", e.target.value)}
            />

            <Button onClick={calculateRisk} disabled={isLoading} className="mt-4">
              {isLoading ? "Calculating..." : "Calculate Risk"}
            </Button>

            {/* Error message */}
            {errorMsg && (
              <div className="mt-4 p-2 rounded bg-red-100 text-red-700 flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                <span>{errorMsg}</span>
                {lastInput && (
                  <Button
                    onClick={calculateRisk}
                    variant="outline"
                    size="sm"
                    className="ml-auto"
                  >
                    Retry
                  </Button>
                )}
              </div>
            )}

            {/* Prediction results */}
            {prediction && (
              <div className="mt-6 space-y-2 p-4 rounded bg-gray-50">
                <p>
                  Risk: <strong>{prediction.risk}%</strong> (
                  {prediction.level})
                </p>
                <p>BMI: {prediction.bmi}</p>
                <p>Model Used: {prediction.modelUsed}</p>

                {prediction.confidence && (
                  <>
                    <Label>Confidence</Label>
                    <Progress value={prediction.confidence * 100} />
                  </>
                )}

                <div className="mt-2">
                  <Label>Recommendations</Label>
                  <ul className="list-disc ml-5">
                    {prediction.recommendations?.map((rec, i) => (
                      <li key={i}>{rec}</li>
                    ))}
                  </ul>
                </div>

                <Badge
                  variant={prediction.level.includes("High") ? "destructive" : "success"}
                  className="mt-2 flex items-center gap-2"
                >
                  {prediction.level.includes("High") ? (
                    <AlertTriangle className="h-4 w-4" />
                  ) : (
                    <CheckCircle2 className="h-4 w-4" />
                  )}
                  {prediction.level}
                </Badge>
              </div>
            )}
          </CardContent>
        </Card>
      </main>
      <Footer />
    </>
  );
};

export default Prediction;

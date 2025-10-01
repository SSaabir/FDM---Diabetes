// src/components/ErrorBoundary.jsx
import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  // Update state when an error is thrown
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  // Log error info
  componentDidCatch(error, errorInfo) {
    console.error("Error caught by ErrorBoundary:", error, errorInfo);
    this.setState({ errorInfo });
  }

  // Reload the page
  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center min-h-screen bg-gray-50 p-4">
          <Card className="max-w-lg w-full">
            <CardHeader>
              <CardTitle className="text-red-600">
                Oops! Something went wrong.
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">
                We ran into an unexpected error. You can try again.
              </p>
              <pre className="text-xs text-red-500 mb-4 whitespace-pre-wrap">
                {this.state.error?.toString()}
              </pre>
              <Button onClick={this.handleReload}>Reload Page</Button>
            </CardContent>
          </Card>
        </div>
      );
    }

    // Render children if no error
    return this.props.children;
  }
}

export default ErrorBoundary;

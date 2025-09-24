import React, { useEffect, useState } from "react";

export default function TermsAndConditions() {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [accepted, setAccepted] = useState(false);
  const [processing, setProcessing] = useState(false);

  // Scroll progress effect
  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = document.documentElement.scrollTop;
      const scrollHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      const progress = (scrollTop / scrollHeight) * 100;
      setScrollProgress(progress);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const acceptTerms = () => {
    setProcessing(true);
    setTimeout(() => {
      setProcessing(false);
      setAccepted(true);
      setTimeout(() => {
        alert("Terms accepted! You can now proceed to the main application.");
      }, 1000);
    }, 500);
  };

  return (
    <div className="bg-[#F3F3E0] text-[#183B4E] font-sans min-h-screen">
      {/* Scroll progress bar */}
      <div className="fixed top-0 left-0 w-full h-1 bg-[#27548A]/20 z-50">
        <div
          className="h-full bg-gradient-to-r from-[#27548A] to-[#DDA853] transition-all duration-100"
          style={{ width: `${scrollProgress}%` }}
        ></div>
      </div>

      <div className="max-w-3xl mx-auto px-4 py-8">
        {/* Warning banner */}
        <div className="bg-gradient-to-r from-[#DDA853] to-[#e6b966] text-white p-6 rounded-xl shadow-lg text-center font-semibold text-lg mb-8">
          ⚠️ This application is for clinical decision support purposes only and
          should not replace professional medical judgment.
        </div>

        {/* Terms & Conditions Card */}
        <div className="bg-white rounded-2xl p-8 mb-6 shadow-xl border-2 border-[#27548A]/10 hover:-translate-y-1 hover:shadow-2xl transition">
          <h2 className="flex items-center gap-3 text-[#27548A] text-2xl font-bold mb-6">
            <div className="w-10 h-10 flex items-center justify-center rounded-lg bg-gradient-to-tr from-[#DDA853] to-[#e6b966]">
              📋
            </div>
            Terms & Conditions
          </h2>
          <ul className="space-y-4">
            <li className="relative bg-[#F3F3E0] p-5 rounded-lg border-l-4 border-[#DDA853] hover:bg-[#dda853]/10 transition">
              <span className="absolute -left-3 top-5 w-6 h-6 rounded-full bg-white border-2 border-[#27548A] flex items-center justify-center text-[#27548A] font-bold">
                ✓
              </span>
              You agree to upload only{" "}
              <strong className="text-[#27548A]">de-identified clinical data</strong>{" "}
              that you are authorized to use.
            </li>
            <li className="relative bg-[#F3F3E0] p-5 rounded-lg border-l-4 border-[#DDA853] hover:bg-[#dda853]/10 transition">
              <span className="absolute -left-3 top-5 w-6 h-6 rounded-full bg-white border-2 border-[#27548A] flex items-center justify-center text-[#27548A] font-bold">
                ✓
              </span>
              <strong className="text-[#27548A]">Predictions are probabilistic estimates</strong>{" "}
              and are meant for clinical decision support only, not as a diagnosis.
            </li>
            <li className="relative bg-[#F3F3E0] p-5 rounded-lg border-l-4 border-[#DDA853] hover:bg-[#dda853]/10 transition">
              <span className="absolute -left-3 top-5 w-6 h-6 rounded-full bg-white border-2 border-[#27548A] flex items-center justify-center text-[#27548A] font-bold">
                ✓
              </span>
              The app provider is <strong className="text-[#27548A]">not responsible</strong> for any
              clinical or treatment decisions made using the outputs.
            </li>
            <li className="relative bg-[#F3F3E0] p-5 rounded-lg border-l-4 border-[#DDA853] hover:bg-[#dda853]/10 transition">
              <span className="absolute -left-3 top-5 w-6 h-6 rounded-full bg-white border-2 border-[#27548A] flex items-center justify-center text-[#27548A] font-bold">
                ✓
              </span>
              Users must{" "}
              <strong className="text-[#27548A]">
                comply with all privacy, data protection, and regulatory
                requirements
              </strong>{" "}
              relevant to their region.
            </li>
            <li className="relative bg-[#F3F3E0] p-5 rounded-lg border-l-4 border-[#DDA853] hover:bg-[#dda853]/10 transition">
              <span className="absolute -left-3 top-5 w-6 h-6 rounded-full bg-white border-2 border-[#27548A] flex items-center justify-center text-[#27548A] font-bold">
                ✓
              </span>
              Data may be stored and processed securely, but users remain{" "}
              <strong className="text-[#27548A]">
                responsible for obtaining proper consents and approvals
              </strong>
              .
            </li>
          </ul>
        </div>

        {/* Privacy Notice */}
        <div className="bg-white rounded-2xl p-8 mb-6 shadow-xl border-2 border-[#27548A]/10 hover:-translate-y-1 hover:shadow-2xl transition">
          <h2 className="flex items-center gap-3 text-[#27548A] text-2xl font-bold mb-6">
            <div className="w-10 h-10 flex items-center justify-center rounded-lg bg-gradient-to-tr from-[#DDA853] to-[#e6b966]">
              🔒
            </div>
            Privacy Notice
          </h2>
          <ul className="space-y-4">
            <li className="relative bg-[#F3F3E0] p-5 rounded-lg border-l-4 border-[#DDA853] hover:bg-[#dda853]/10 transition">
              <span className="absolute -left-3 top-5 w-6 h-6 rounded-full bg-white border-2 border-[#27548A] flex items-center justify-center text-[#27548A] font-bold">
                ✓
              </span>
              <strong className="text-[#27548A]">No personally identifiable information</strong>{" "}
              should be uploaded.
            </li>
            <li className="relative bg-[#F3F3E0] p-5 rounded-lg border-l-4 border-[#DDA853] hover:bg-[#dda853]/10 transition">
              <span className="absolute -left-3 top-5 w-6 h-6 rounded-full bg-white border-2 border-[#27548A] flex items-center justify-center text-[#27548A] font-bold">
                ✓
              </span>
              All uploaded data is processed in a{" "}
              <strong className="text-[#27548A]">secure and privacy-preserving manner</strong>.
            </li>
            <li className="relative bg-[#F3F3E0] p-5 rounded-lg border-l-4 border-[#DDA853] hover:bg-[#dda853]/10 transition">
              <span className="absolute -left-3 top-5 w-6 h-6 rounded-full bg-white border-2 border-[#27548A] flex items-center justify-center text-[#27548A] font-bold">
                ✓
              </span>
              Data is used{" "}
              <strong className="text-[#27548A]">only for generating predictions</strong> and is not
              shared with third parties.
            </li>
          </ul>
        </div>

        {/* Disclaimer */}
        <div className="bg-white rounded-2xl p-8 mb-6 shadow-xl border-2 border-[#27548A]/10 hover:-translate-y-1 hover:shadow-2xl transition">
          <h2 className="flex items-center gap-3 text-[#27548A] text-2xl font-bold mb-6">
            <div className="w-10 h-10 flex items-center justify-center rounded-lg bg-gradient-to-tr from-[#DDA853] to-[#e6b966]">
              ⚖️
            </div>
            Disclaimer
          </h2>
          <ul className="space-y-4">
            <li className="relative bg-[#F3F3E0] p-5 rounded-lg border-l-4 border-[#DDA853] hover:bg-[#dda853]/10 transition">
              <span className="absolute -left-3 top-5 w-6 h-6 rounded-full bg-white border-2 border-[#27548A] flex items-center justify-center text-[#27548A] font-bold">
                ✓
              </span>
              This tool is a{" "}
              <strong className="text-[#27548A]">prototype for educational and research purposes</strong>.
            </li>
            <li className="relative bg-[#F3F3E0] p-5 rounded-lg border-l-4 border-[#DDA853] hover:bg-[#dda853]/10 transition">
              <span className="absolute -left-3 top-5 w-6 h-6 rounded-full bg-white border-2 border-[#27548A] flex items-center justify-center text-[#27548A] font-bold">
                ✓
              </span>
              It should{" "}
              <strong className="text-[#27548A]">not replace professional medical judgment</strong>.
            </li>
            <li className="relative bg-[#F3F3E0] p-5 rounded-lg border-l-4 border-[#DDA853] hover:bg-[#dda853]/10 transition">
              <span className="absolute -left-3 top-5 w-6 h-6 rounded-full bg-white border-2 border-[#27548A] flex items-center justify-center text-[#27548A] font-bold">
                ✓
              </span>
              Always{" "}
              <strong className="text-[#27548A]">
                confirm predictions with a licensed healthcare provider
              </strong>{" "}
              before making treatment decisions.
            </li>
          </ul>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap justify-center gap-4 mt-10">
          <button
            onClick={scrollToTop}
            className="px-6 py-3 rounded-lg border-2 border-[#27548A] text-[#27548A] font-semibold text-lg hover:bg-[#27548A] hover:text-white transition w-40"
          >
            Review Again
          </button>
          <button
            onClick={acceptTerms}
            disabled={processing || accepted}
            className={`px-6 py-3 rounded-lg font-semibold text-lg w-52 transition ${
              accepted
                ? "bg-gradient-to-r from-green-600 to-green-400 text-white"
                : "bg-gradient-to-r from-[#27548A] to-[#183B4E] text-white hover:shadow-xl hover:-translate-y-1"
            }`}
          >
            {processing
              ? "Processing..."
              : accepted
              ? "✓ Terms Accepted"
              : "Accept & Continue"}
          </button>
        </div>
      </div>
    </div>
  );
}



function AboutUs() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#F3F3E0] p-8">
      <div className="bg-white shadow-lg rounded-2xl p-10 max-w-2xl text-center border-t-8 border-[#27548A]">
        <h1 className="text-4xl font-bold text-[#183B4E] mb-4">
          About Us
        </h1>
        <p className="text-lg text-gray-700 leading-relaxed mb-6">
          Welcome to our Diabetes Risk Predictor! Our platform is designed to help 
          individuals take proactive steps in managing their health. By analyzing key 
          health indicators, we provide insights into potential diabetes risks and 
          guide users toward healthier lifestyle choices. Our mission is to empower 
          people with knowledge, simplify health tracking, and make preventive care 
          accessible for everyone.
        </p>
        
        <div className="mt-6 text-[#DDA853] font-semibold">
          Empowering You Through Technology
        </div>
      </div>
    </div>
  );
}

export default AboutUs;

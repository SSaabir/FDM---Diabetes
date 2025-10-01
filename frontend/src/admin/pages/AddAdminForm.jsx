import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserPlus } from 'lucide-react';

const AddAdminForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    position: '',
    contact: '',
    email: '',
    password: '',
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // ✅ TODO: Replace with backend API call to add admin
    console.log('New Admin Data:', formData);
    alert('Admin added successfully!');
    navigate('/AdminDashboard'); // Redirect back to dashboard
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#F3F3E0] via-[#E6EAD0] to-[#C6DCBA] flex items-center justify-center p-6">
      <div className="bg-white shadow-2xl rounded-2xl p-8 w-full max-w-lg transition-transform hover:scale-[1.01]">
        {/* Header */}
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-2 bg-[#27548A] rounded-full text-white">
            <UserPlus size={20} />
          </div>
          <h2 className="text-2xl font-bold text-[#183B4E]">Add New Admin</h2>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Full Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="Enter full name"
              className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#27548A] transition"
            />
          </div>

          {/* Position */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Position</label>
            <input
              type="text"
              name="position"
              value={formData.position}
              onChange={handleChange}
              required
              placeholder="eg : System Admin, Data Analyst"
              className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#27548A] transition"
            />
          </div>

          {/* Contact Number */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Contact Number</label>
            <input
              type="tel"
              name="contact"
              value={formData.contact}
              onChange={handleChange}
              required
              placeholder="eg : +94 77 123 4567"
              className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#27548A] transition"
            />
          </div>

          {/* Email */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="admin@example.com"
              className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#27548A] transition"
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter a strong password"
              className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#27548A] transition"
            />
          </div>

          {/* Buttons */}
          <div className="flex space-x-3 pt-4">
            <button
              type="submit"
              className="flex-1 px-4 py-3 bg-[#27548A] text-white rounded-lg hover:bg-[#183B4E] transition-colors font-medium"
            >
              Add Admin
            </button>
            <button
              type="button"
              onClick={() => navigate('/AdminDashboard')}
              className="flex-1 px-4 py-3 bg-gray-200 text-[#183B4E] rounded-lg hover:bg-gray-300 transition-colors font-medium"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddAdminForm;

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const API = "http://127.0.0.1:8000";

function RegisterPage() {

  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const registerUser = async () => {

    if (!name || !email) {
      alert("Please fill all fields");
      return;
    }

    try {

      const res = await axios.post(
        `${API}/users/`,
        {
          full_name: name,
          email: email
        }
      );

      localStorage.setItem(
        "user_id",
        res.data.id
      );

      localStorage.setItem(
        "email",
        email
      );

      navigate("/verify");

    } catch (error) {

      console.error(error);

      alert("Registration failed");

    }

  };
  return (
    <div className="page">

      <div className="card onboarding-card">

        <div className="step-badge">
          STEP 1 OF 2
        </div>

        <h1>
          Connect Your Workspace
        </h1>

        <p>
          Choose the Google services MailMind can
          manage on your behalf.
        </p>

        <div className="form-group">

          <label>
            Full Name
          </label>

          <input
            type="text"
            placeholder="Enter your full name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

        </div>

        <div className="form-group">

          <label>
            Gmail Address
          </label>

          <input
            type="email"
            placeholder="you@gmail.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

        </div>

        <h3 className="section-title">
          Services to Enable
        </h3>

        <div className="service-options">

          <div className="service-option">
            <span>📧</span>

            <div>
              <strong>Gmail Cleanup</strong>
              <p>Delete OTP and promotional emails</p>
            </div>

            <input
              type="checkbox"
              defaultChecked
            />
          </div>

          <div className="service-option">
            <span>📅</span>

            <div>
              <strong>Calendar Sync</strong>
              <p>Automatically create reminders</p>
            </div>

            <input
              type="checkbox"
              defaultChecked
            />
          </div>

          <div className="service-option">
            <span>📁</span>

            <div>
              <strong>Drive Backup</strong>
              <p>Store attachments securely</p>
            </div>

            <input
              type="checkbox"
              defaultChecked
            />
          </div>

          <div className="service-option">
            <span>📊</span>

            <div>
              <strong>AI Reports</strong>
              <p>AI productivity insights and summaries</p>
            </div>

            <input
              type="checkbox"
              defaultChecked
            />
          </div>

        </div>
        <p className="security-note">
          🔒 Your data remains private and encrypted.
        </p>
        <button
          className="primary-btn"
          onClick={registerUser}
        >
          Connect Workspace

        </button>

      </div>

    </div>
  );
}

export default RegisterPage;
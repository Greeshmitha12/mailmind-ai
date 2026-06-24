import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const API = "http://127.0.0.1:8000";

function VerifyOTPPage() {

  const navigate = useNavigate();

  const [otp, setOtp] = useState("");
  const [captchaInput, setCaptchaInput] = useState("");

  const captcha = "A7K9X";

  const handleVerify = async () => {

    const email = localStorage.getItem("email");

    if (!otp) {
      alert("Please enter OTP");
      return;
    }

    if (captchaInput !== captcha) {
      alert("Invalid CAPTCHA");
      return;
    }

    try {

      const res = await axios.post(
        `${API}/verify`,
        {
          email,
          otp
        }
      );

      alert(res.data.message);

      if (
        res.data.message ===
        "Email verified successfully"
      ) {
        navigate("/dashboard");
      }

    } catch (error) {

      console.error(error);
      alert("OTP verification failed");

    }
  };

  return (
    <div className="page-center">

      <div className="card otp-modern-card">

        <div className="step-badge">
          STEP 2 OF 2
        </div>

        <div className="otp-icon">
          🔐
        </div>

        <h1>
          Verify Your Email
        </h1>

        <p>
          We sent a 6-digit verification code to
          <br />
          <strong>
            {localStorage.getItem("email")}
          </strong>
        </p>

        <div className="form-group">

          <label>
            One-Time Password
          </label>

          <input
            className="otp-input"
            type="text"
            placeholder="Enter OTP"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
          />

        </div>

        <div className="captcha-wrapper">

          <label>
            Security Check
          </label>

          <div className="captcha-box">
            {captcha}
          </div>

        </div>

        <div className="form-group">

          <input
            type="text"
            placeholder="Enter CAPTCHA"
            value={captchaInput}
            onChange={(e) =>
              setCaptchaInput(
                e.target.value.toUpperCase()
              )
            }
          />

          <p className="resend-text">
            Didn't receive the code?
            <span> Resend OTP</span>
          </p>

        </div>

        <p className="security-note">
          🔒 Verification helps protect your workspace.
        </p>

        <button
          className="primary-btn"
          onClick={handleVerify}
        >
          Verify & Continue
        </button>

      </div>

    </div>
  );
}

export default VerifyOTPPage;
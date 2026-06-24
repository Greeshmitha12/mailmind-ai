import { useNavigate } from "react-router-dom";

function LoginPage() {

  const navigate = useNavigate();

  return (
    <div className="page-center">

      <div className="glass-card">

        <img
          src="/mailmind_logo.png"
          alt="MailMind"
          className="hero-logo"
        />

        <h1 className="login-title">
          AI-Powered Email Workspace
        </h1>

        <p className="login-subtitle">
          Automate Gmail, Calendar and Drive with AI.
        </p>

       <button
        className="primary-btn"
        onClick={() => navigate("/register")}
      >
        Get Started
       </button>
         <div className="feature-row">
          <span>📧 Gmail Cleanup</span>
          <span>📅 Calendar Sync</span>
          <span>📁 Drive Backup</span>
          <span>🤖 AI Reports</span>
        </div>
        <p className="footer-text">
            Built for students, professionals and job seekers.
        </p>

      </div>

    </div>
  );
}

export default LoginPage;
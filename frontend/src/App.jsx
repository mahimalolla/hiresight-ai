import { useState } from "react";
import axios from "axios";

export default function App() {
  const [githubUrl, setGithubUrl] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async (e) => {
    e.preventDefault();

    if (!resumeFile || !githubUrl || !jobDescription) {
      setError("Please upload a resume, enter a GitHub username, and paste a job description.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", resumeFile);
      formData.append("github_url", githubUrl);
      formData.append("job_description", jobDescription);

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze/full-match",
        formData
      );

      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Something went wrong while analyzing the candidate.");
    } finally {
      setLoading(false);
    }
  };

  const match = result?.match_result;
  const resumeSummary = result?.resume_summary;
  const githubSummary = result?.github_summary;
  const candidateProfile = result?.candidate_profile;

  return (
    <div className="app-shell">
      <div className="page">
        <header className="hero">
          <div>
            <div className="eyebrow">AI Hiring Intelligence</div>
            <h1>HireSight</h1>
            <p>
              Analyze candidate fit using resume evidence, GitHub activity, and
              role requirements.
            </p>
          </div>
        </header>

        <div className="layout">
          <section className="panel input-panel">
            <h2>Analyze Candidate</h2>

            <form onSubmit={handleAnalyze} className="form">
              <label>
                Resume PDF
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(e) => setResumeFile(e.target.files[0])}
                />
              </label>

              <label>
                GitHub Username or URL
                <input
                  type="text"
                  value={githubUrl}
                  onChange={(e) => setGithubUrl(e.target.value)}
                  placeholder="mahimalolla or https://github.com/mahimalolla"
                />
              </label>

              <label>
                Job Description
                <textarea
                  rows="10"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  placeholder="Paste the role description here..."
                />
              </label>

              <button type="submit" disabled={loading}>
                {loading ? "Analyzing..." : "Analyze Candidate"}
              </button>
            </form>

            {error && <p className="error">{error}</p>}
          </section>

          <section className="panel results-panel">
            <div className="results-header">
              <h2>Candidate Report</h2>
              <span className="status-pill">
                {result ? "Analysis Complete" : "Waiting for Input"}
              </span>
            </div>

            {!result && !loading && (
              <div className="empty-state">
                <h3>No analysis yet</h3>
                <p>
                  Upload a resume, enter a GitHub profile, and paste a job
                  description to generate a candidate match report.
                </p>
              </div>
            )}

            {result && (
              <div className="results-stack">
                <div className="score-card">
                  <div>
                    <div className="score-label">Overall Match Score</div>
                    <div className="score-value">{match?.match_score ?? 0}%</div>
                  </div>
                  <div className="score-recommendation">
                    {match?.recommendation || "No Recommendation"}
                  </div>
                </div>

                <div className="two-col">
                  <div className="sub-card">
                    <h3>Matched Skills</h3>
                    <div className="tag-wrap">
                      {match?.matched_skills?.length ? (
                        match.matched_skills.map((skill) => (
                          <span key={skill} className="tag success">
                            {skill}
                          </span>
                        ))
                      ) : (
                        <p className="muted">No matched skills found.</p>
                      )}
                    </div>
                  </div>

                  <div className="sub-card">
                    <h3>Missing Skills</h3>
                    <div className="tag-wrap">
                      {match?.missing_skills?.length ? (
                        match.missing_skills.map((skill) => (
                          <span key={skill} className="tag danger">
                            {skill}
                          </span>
                        ))
                      ) : (
                        <p className="muted">No major gaps found.</p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="sub-card">
                  <h3>Resume Skills</h3>
                  <div className="tag-wrap">
                    {resumeSummary?.skills?.length ? (
                      resumeSummary.skills.map((skill) => (
                        <span key={skill} className="tag neutral">
                          {skill}
                        </span>
                      ))
                    ) : (
                      <p className="muted">No resume skills extracted.</p>
                    )}
                  </div>
                </div>

                <div className="two-col">
                  <div className="sub-card">
                    <h3>GitHub Summary</h3>
                    <div className="info-list">
                      <p><strong>Name:</strong> {githubSummary?.name || "N/A"}</p>
                      <p><strong>Username:</strong> {githubSummary?.username || "N/A"}</p>
                      <p><strong>Public Repos:</strong> {githubSummary?.public_repos ?? 0}</p>
                      <p><strong>Followers:</strong> {githubSummary?.followers ?? 0}</p>
                      <p><strong>AI Signal Score:</strong> {githubSummary?.ai_signal_score || "N/A"}</p>
                    </div>
                  </div>

                  <div className="sub-card">
                    <h3>Candidate Profile Skills</h3>
                    <div className="tag-wrap">
                      {candidateProfile?.combined_skills?.length ? (
                        candidateProfile.combined_skills.map((skill) => (
                          <span key={skill} className="tag neutral">
                            {skill}
                          </span>
                        ))
                      ) : (
                        <p className="muted">No candidate profile skills found.</p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="sub-card">
                  <h3>Fit Summary</h3>
                  <p className="summary-text">
                    HireSight identified a{" "}
                    <strong>{match?.recommendation?.toLowerCase() || "candidate fit"}</strong>{" "}
                    with strong evidence in{" "}
                    <strong>{match?.matched_skills?.slice(0, 3).join(", ") || "key skills"}</strong>.
                    Current gaps include{" "}
                    <strong>{match?.missing_skills?.join(", ") || "no major gaps"}</strong>.
                  </p>
                </div>
              </div>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}
import { prioritizeFeedback, calculateFeedbackScore } from './priorityLogic';

export const FeedbackPriority = ({ feedbackList }) => {
  const [prioritizedFeedback, setPrioritizedFeedback] = useState([]);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    try {
      const prioritized = prioritizeFeedback(feedbackList);
      setPrioritizedFeedback(prioritized);
    } catch (err) {
      setError('Error prioritizing feedback');
    }
  }, [feedbackList]);

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <div className="feedback-priority-container">
      <h2>Feedback Prioritization</h2>
      {prioritizedFeedback.length === 0 ? (
        <p>No feedback to prioritize.</p>
      ) : (
        <ul className="priority-list">
          {prioritizedFeedback.map((feedback, index) => (
            <li key={feedback.id} className={`priority-level-${index + 1}`}></li>
          ))}
        </ul>
      )}
    </div>
  );
};
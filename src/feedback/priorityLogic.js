export const prioritizeFeedback = (feedbackItems) => {
  return feedbackItems.sort((a, b) => {
    // Calculate priority score for each item
    const scoreA = calculateFeedbackScore(a);
    const scoreB = calculateFeedbackScore(b);
    
    // Sort by score (highest first)
    return scoreB - scoreA;
  });
};

export const calculateFeedbackScore = (feedback) => {
  // Base score
  let score = 0;
  
  // Severity weighting (0-2)
  switch (feedback.severity) {
    case 'critical':
      score += 2;
      break;
    case 'high':
      score += 1.5;
      break;
    case 'medium':
      score += 1;
      break;
    case 'low':
      score += 0.5;
      break;
  }', 
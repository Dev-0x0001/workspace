export async function fetchReviewStatus(projectId) {
  try {
    const response = await fetch(`/api/review/status/${projectId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Failed to fetch review status: ${error.message}`);
    return { status: 'error', message: error.message };
  }
}

export async function approveFramework(projectId) {
  try {
    const response = await fetch(`/api/review/approve/${projectId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Failed to approve framework: ${error.message}`);
    return { status: 'error', message: error.message };
  }
}

export async function rejectFramework(projectId, reasons) {
  try {
    const response = await fetch(`/api/review/reject/${projectId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ reasons }),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Failed to reject framework: ${error.message}`);
    return { status: 'error', message: error.message };
  }
}
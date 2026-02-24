<template>
  <div class="feedback-interface">
    <!-- Feedback List -->
    <div class="feedback-list">
      <feedback-item
        v-for="feedback in feedbacks"
        :key="feedback.id"
        :feedback="feedback"
        @mark-read="markAsRead"
      />
    </div>

    <!-- Feedback Detail -->
    <div class="feedback-detail">
      <feedback-detail
        :feedback="selectedFeedback"
        v-if="selectedFeedback"
      />
    </div>

    <!-- Action Buttons -->
    <div class="actions">
      <button @click="createNewFeedback">Create New</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      feedbacks: [],
      selectedFeedback: null
    }
  },
  methods: {
    async loadFeedbacks() {
      // Implementation
    },
    markAsRead(id) {
      // Implementation
    }
  }
}
</script>

<style>
.feedback-interface {
  display: flex;
  height: 100%;
}

.feedback-list {
  flex: 1;
  overflow-y: auto;
}

.feedback-detail {
  flex: 2;
  padding: 20px;
}
</style>
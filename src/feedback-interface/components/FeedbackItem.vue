<template>
  <div class="feedback-item" :class="{ 'read': feedback.read }">
    <div class="header">
      <h3>{{ feedback.title || 'Untitled Feedback' }}</h3>
      <span class="priority">{{ getPriorityLabel(feedback.priority) }}</span>
    </div>
    <div class="content">
      {{ feedback.content }}
    </div>
    <div class="actions">
      <button @click="toggleRead">{{ feedback.read ? 'Unread' : 'Read' }}</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    feedback: {
      type: Object,
      required: true
    }
  },
  methods: {
    toggleRead() {
      this.$emit('mark-read', this.feedback.id)
    },
    getPriorityLabel(priority) {
      switch (priority) {
        case 'critical': return 'Critical ⚠️';
        case 'high': return 'High ⚠️';
        case 'medium': return 'Medium ⚠️';
        case 'low': return 'Low ⚠️';
        default: return 'Pending';
      }
    }
  }
}
</script>

<style>
.feedback-item {
  border: 1px solid #eee;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 4px;
}

.feedback-item.read {
  background: #f0f0f0;
}
</style>
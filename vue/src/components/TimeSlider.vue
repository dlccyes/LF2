<script>
export default {
  data() {
    return {
      timeRange: 30,
    }
  },
  watch: {
    timeRange(newVal, oldVal) {
      timeRange = this.timeRange;
    }
  },
}
</script>

<template>
<div class="input_area">
  <span>Seek time to how many minutes before?</span>
  <div class="row">
    <input v-model="timeRange" type="range" id="timeRange" min='0' max='6000' step='1'>
    <span><span id="timeRangeVal">{{ timeRange }}</span>m</span>
  </div>
</div>
</template>
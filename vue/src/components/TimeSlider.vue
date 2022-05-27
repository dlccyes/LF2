<script>
import { globeStore } from '@/stores/globe'

export default {
  data() {
    return {
      timeRange: globeStore().timeRange,
    }
  },
  watch: {
    timeRange(newVal, oldVal) {
      globeStore().timeRange = newVal;
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
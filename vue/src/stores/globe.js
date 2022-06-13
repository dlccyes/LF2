// define global variables

import { defineStore } from 'pinia'

export const globeStore = defineStore({
  state: () => {
    return {
      timeRange: 10, // value of time slider
      night: 1,
      update: 0, // value change -> rerun some functions
    }
  },
})
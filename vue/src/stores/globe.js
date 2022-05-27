// define global variables

import { defineStore } from 'pinia'

export const globeStore = defineStore({
  state: () => {
    return {
      timeRange: 30,
      night: 1,
    }
  },
})
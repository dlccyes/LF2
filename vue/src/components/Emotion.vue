<script>
import axios from 'axios';
import { drawLine, drawCloud } from '@/helper.js';
import { globeStore } from '@/stores/globe'

export default {
  data() {
    return {
      currentEmotionDivHtml: '',
      emotionGraphDivHtml: '',
      emotionCloudDivHtml: '',
      globe:  globeStore(),
    }
  },
  methods: {
    // calculate average emotion score given the input json, on the scale of 5
    calEmoScore(emoJson){
      var emoScoreMap = {'surprise':5, 'happy': 5, 'neutral': 3, 'sad': 2, 'fear':0, 'disgust':1, 'contempt':1, 'anger':0};
      var emoScore = 0;
      var emotionDataNum = 0;
      for(var emo in emoJson){ // a json
        if(!emoScoreMap[emo]){
          continue;
        }
        emotionDataNum += emoJson[emo].length;
        emoScore += emoScoreMap[emo]*emoJson[emo].length;
      }
      if(emotionDataNum == 0){
        return null;
      }
      emoScore /= emotionDataNum;
      emoScore = parseFloat(emoScore.toFixed(2)); // round to 2 decimal places
      return emoScore;
    },
    getEmotion(){
      var self = this;
      var objData = {
        'time_range': this.globe.timeRange
      };
      axios.post('/emotion', objData)
      .then(function(result){
        console.log(result);
        var emotionData = result.data.data.emotion;
        var emotionDataNum = emotionData.length;
        var currentEmotionDivHtml = '';
        if(emotionDataNum == 0){
          currentEmotionDivHtml += 'No emotion data.';
        }else{
          var emoScore = self.calEmoScore(emotionData[emotionDataNum-1]['emotions']);
          currentEmotionDivHtml += 'Current classroom positivity: '+ emoScore +' out of 5';
        }
        self.currentEmotionDivHtml = currentEmotionDivHtml;
        if(emotionDataNum < 2){
          self.emotionGraphDivHtml = 'Not enough data to show emotion graph.';
          self.emotionCloudDivHtml = '';
        }else{
          self.emotionGraphDivHtml = '';
          var emotionVsTimeArr = [];
          var emotionFreqJson = {};
          for(var item of emotionData){
            var emotionJson = item['emotions'];
            emotionVsTimeArr.push([new Date(item['log_time']), self.calEmoScore(emotionJson)]);
            for(var emo in emotionJson){
              if(!emotionFreqJson[emo]){
                emotionFreqJson[emo] = 0;
              }
              emotionFreqJson[emo] += emotionJson[emo].length;
            }
          }
          var yAx;
          drawLine(emotionVsTimeArr, 'emotionGraphDiv', 'log time', 'positivity', yAx=[0, 5, 1]);
          var emotionCloudData = [];
          for(var emo in emotionFreqJson){ // convert into anychart data format
            emotionCloudData.push({'x':emo, 'value':emotionFreqJson[emo]});
          }
          drawCloud(emotionCloudData, 'emotionCloudDiv');
        }
      });
    },
    refresh() {
      this.getEmotion();
    },
  },
  mounted() {
    this.refresh();
  },
  computed: {
    update(){
      return this.globe.update;
    },
  },
  watch: {
    update(){
      this.refresh();
    },
  }
}
</script>

<template>

<div id="currentEmotionDiv">{{ currentEmotionDivHtml }}</div>
<div id="emotionGraphDiv">{{ emotionGraphDivHtml }}</div>
<div id="emotionCloudDiv">{{ emotionCloudDivHtml }}</div>

</template>
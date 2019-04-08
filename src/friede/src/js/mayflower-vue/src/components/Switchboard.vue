<template lang="html">
  <div class="switchboard">
    <transition mode="in-out">
      <vk-grid  v-if="matches.length || locations.length"
                gutter="small" class="display uk-child-width-1-8m">
        <div v-for="match in matches">{{ match }}</div>
      </vk-grid>
    </transition>
  </div>
</template>

<script lang="js">
import { Grid } from 'vuikit/lib/grid';
export default  {
  name: 'switchboard',
  props: {
    matches: {
      type: Array,
      default: () => []
    },
    locations: {
      type: Array,
      default: () => []
    }
  },
  components: {
    'vk-grid': Grid,
  },
  mounted() {
    
  },
  data() {
    return {
      
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
.switchboard {
  .display{
    position: fixed;
    bottom: 42px;
    left: 24px;
    right: 10px;
    background: rgba(0,0,0,0.75);
    color: white;
    border-radius: 4px;
    padding: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3)
  }
}
</style>

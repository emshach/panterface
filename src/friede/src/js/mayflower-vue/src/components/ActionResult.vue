<template lang="html">
  <div class="action-result">
    <h4>{{ action.name }} Results</h4>
    <ul uk-accordion>
      <li v-for="( result, id ) in results" class="action-operand">
        <a class="uk-accordion-title" href="#">{{ objects[ id ].path }}</a>
        <div class="uk-accordion-content">
          <h5>Outcome</h5>
          <div class="content-outcome" >{{ result.res || 'None' }}</div>
          <h5>Log</h5>
          <div class="content-log">{{ result.out || 'None' }}</div>
          <h5>Errors/Warnings</h5>
          <div class="content-err">{{ result.err || 'None' }}</div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script lang="js">
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
export default  {
  name: 'ActionResult',
  components: {
    FontAwesomeIcon
  },
  props: {
    action: {
      type: Object,
      default: () => ({})
    },
    objects: {
      type: Object,
      default: () => ({})
    },
    results: {
      type: Object,
      default: () => ({})
    }
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
.action-result {
  > h3 {
    text-transform: capitalize;
  }
}
</style>

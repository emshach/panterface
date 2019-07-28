<template lang="html">
  <div class="action-result">
    <h4>{{ action.name }} Results</h4>
    <div v-if="!results" class="error">No response</div>
    <div v-else-if="'error' in results" class="error" v-html="results.error" />
    <ul v-else uk-accordion>
      <li v-for="( result, id ) in results" :class=itemClass>
        <a class="uk-accordion-title" href="#">{{ objects[ id ].path }}</a>
        <div class="uk-accordion-content">
          <h5>Outcome</h5>
          <template v-if="result.res">
            <div v-if="result.res.success" class="content-outcome success" >{{
              result.res.success }}</div>
            <div v-else-if="result.res.error" class="content-outcome error" >{{
              result.res.error }}</div>
            <div v-else class="content-outcome" >{{ result.res }}</div>
          </template>
          <div v-else class="content-outcome" >None</div>
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
export default {
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
  mounted() {},
  data() {
    return {}
  },
  methods: {},
  computed: {
    itemClass() {
      return {
        'action-operand': true,
        'uk-open': Object.keys( this.results ).length === 1
      };
    }
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

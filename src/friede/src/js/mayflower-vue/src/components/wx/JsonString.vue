<template lang="html">
  <span class="json-string">
    <span class="json-delim">"</span>
    <textarea v-if="editing" v-model="_value" @input="input" @change="input" />
    <template v-else>
      <span class="json-string-content" v-html="html" />
      <span v-if="truncated" class="json-elipses">...</span>
      <vk-btn v-if="this._value.length > 40" class="json-collapse" type="light"
              @click.prevent="collapse=!collapse">
        <font-awesome-icon :icon="collapse ? 'plus' : 'minus' " />
      </vk-btn>
    </template>
    <span class="json-delim">"</span>
  </span>
</template>

<script lang="js">
import { Button as VkBtn } from 'vuikit/lib/button'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'
import { JsonWidgetMixin } from '@/lib/mixins'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add( faPlus, faMinus )

export default  {
  name: 'JsonString',
  mixins: [ JsonWidgetMixin ],
  components: { VkBtn },
  props: [],
  mounted() {
    
  },
  data() {
    return {
      truncated: false
    }
  },
  methods: {
    
  },
  computed: {
    html() {
      const s = this._value.replace(
        /((?:\\\\)*)\\n/g, ( $0, $1 ) => `${$1}<br/>\n` );
      if ( collapse && this._value.length > 40 ) {
        this.truncated = true;
        return s.slice( 0, 40 );
      }
      this.truncated = false;
      return s;
    }
  }
}
</script>

<style scoped lang="scss">
  .json-string {

  }
</style>

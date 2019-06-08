<template lang="html">
  <span class="json-string">
    <span class="json-delim">"</span>
    <textarea v-if="editing" :value="value" ref="input"
              @blur="commit" @input="input" @change="input" />
    <template v-else>
      <span class="json-string-content" v-html="html"
            @click.prevent="editMode = true" />
      <span v-if="truncated" class="json-elipses">...</span>
      <vk-btn v-if="this.value.length > 40" class="json-collapse" type="light"
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
  props: {
    value: {
      type: String,
      default: ''
    }
  },
  mounted() {
    
  },
  data() {
    return {
      truncated: false,
      collapse: false,
    }
  },
  methods: {
    input() {
      this.$emit( 'input', this.$refs.input.value );
    },
    commit() {
      this.editMode = false;
    },
  },
  computed: {
    html() {
      const s = this.value.replace(
        /((?:\\\\)*)\\n/g, ( $0, $1 ) => `${$1}<br/>\n` );
      if ( this.collapse && this.value.length > 40 ) {
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

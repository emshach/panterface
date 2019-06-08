<template lang="html">
  <span class="json-widget">
    <vk-btn class="json-type-chooser" type="text">{{ types[ type ].symbol}}</vk-btn>
    <template v-if="editing">
      <vk-btn class="json-type-chooser" type="text">{{ types[ type ].symbol}}</vk-btn>
      <vk-dropdown>
        <vk-btn v-for="( a, i ) in actions" :key="i"
                @click.prevent="setType(a)">{{ a.label }}</vk-btn>
      </vk-dropdown>
    </template>
    <component :is="tag" :readonly="readonly" :value="_value" />
  </span>
</template>

<script lang="js">
import isPlainObject from 'lodash/isPlainObject'
import isArray from 'lodash/isArray'
import isNumber from 'lodash/isNumber'
import isString from 'lodash/isString'
import isBoolean from 'lodash/isBoolean'
import isNull from 'lodash/isNull'
import { Button as VkBtn } from 'vuikit/lib/button'
import { Dropdown as VkDropdown } from 'vuikit/lib/dropdown'
import components from './json'
export default  {
  name: 'JsonWidget',
  components: {
    VkBtn,
    VkDropdown,
    ...components
  },
  props: {
    value: {
      type: [ Object, Array, Number, String, Boolean ],
      default: null
    },
    readonly: {
      type: Boolean,
      default: true
    },
  },
  created() {
    this.updateVal();
  },
  data() {
    return {
      _value: null,
      types: {
        object: {
          label: 'Object',
          symbol: '{}',
        },
        array: {
          label: 'Array',
          symbol: '[]',
        },
        number: {
          label: 'Number',
          symbol: '#',
        },
        string: {
          label: 'String',
          symbol: '""',
        },
        boolean: {
          label: 'Boolean',
          symbol: '&',
        },
        null: {
          label: 'Null',
          symbol: '()',
        },
        invalid: {
          label: 'Invalid',
          symbol: '!',
        },
        unknown: {
          label: 'Unknown',
          symbol: '?',
        }
      },
      type: 'null',
    }
  },
  methods: {
    getType(v) {
      return (
        isPlainObject(v) ? 'object'
           : isArray(v) ? 'array'
           : isNumber(v) ? 'number'
           : isString(v) ? 'string'
           : isBoolean(v) ? 'boolean'
           : isNull(v) ? 'null'
           : 'invalid'
      );
    },
    updateVal() {
      const v = this.value;
      this.type = this.getType(v);
      this._value = v;
    },
    setType( action ) {
      this.type = action.type;
      const v = action.op( this._value );
      if ( this.type === 'unknown' )
        this.type = this.getType(v);
      this._value = v;
      this.$emit( 'input', this._value );
      this.$emit( 'change', this._value );
    },
    toObjectKey( val ) {
      var o = {}
      o[ val ] = null;
      return o;
    }
  },
  computed: {
    editing() {
      return !this.readonly && this.editMode;
    },
    tag() {
      return 'json-' + this.type;
    },
    actions() {
      const t = this.type;
      return [].concat(
        t == 'object' ? [
          {
            label: 'to object value',
            type: 'object',
            op: x => ({ '': x }),
          },
          {
            label: 'clear',
            type: 'object',
            op: () => ({}),
          },
          {
            label: 'to array element',
            type: 'array',
            op: x => [x],
          },
          {
            label: 'array of keys',
            type: 'array',
            op: Object.keys,
          },
          {
            label: 'array of values',
            type: 'array',
            op: Object.values,
          },
          {
            label: 'array of [key, val]',
            type: 'array',
            op: x => Object.keys(x).map( k => [ k, x[k] ]),
          },
          {
            label: 'array of {key, value}',
            type: 'array',
            op: x => Object.keys(x).map( k => ({ key:k, value: x[k] })),
          },
          {
            label: 'array',
            type: 'array',
            op: () => [],
          },
          {
            label: 'to entry count',
            type: 'number',
            op: x => Object.keys(x).length,
          },
          {
            label: 'number',
            type: 'number',
            op: () => 0,
          },
          {
            label: 'serialize',
            type: 'string',
            op: JSON.stringify,
          },
          {
            label: 'string',
            type: 'string',
            op: () => '',
          },
          {
            label: 'true',
            type: 'boolean',
            op: () => true,
          },
          {
            label: 'false',
            type: 'boolean',
            op: () => false,
          },
          {
            label: 'null',
            type: 'null',
            op: () => null,
          },
        ]
        : t == 'array' ? [
          {
            label: 'to object value',
            type: 'object',
            op: x => ({ '': x }),
          },
          {
            label: 'object',
            type: 'object',
            op: () => ({}),
          },
          {
            label: 'to array element',
            type: 'array',
            op: x => [x],
          },
          {
            label: 'clear',
            type: 'array',
            op: () => [],
          },
          {
            label: 'to length',
            type: 'number',
            op: x => x.length,
          },
          {
            label: 'number',
            type: 'number',
            op: () => 0,
          },
          {
            label: 'serialize',
            type: 'string',
            op: JSON.stringify,
          },
          {
            label: 'string',
            type: 'string',
            op: () => '',
          },
          {
            label: 'true',
            type: 'boolean',
            op: () => true,
          },
          {
            label: 'false',
            type: 'boolean',
            op: () => false,
          },
          {
            label: 'null',
            type: 'null',
            op: () => null,
          },
        ]
        : t == 'number' ? [
          {
            label: 'to object value',
            type: 'object',
            op: x => ({ '': x }),
          },
          {
            label: 'to object key',
            type: 'object',
            op: this.toObjectKey,
          },
          {
            label: 'object',
            type: 'object',
            op: () => ({}),
          },
          {
            label: 'to array element',
            type: 'array',
            op: x => [x],
          },
          {
            label: 'array',
            type: 'array',
            op: () => [],
          },
          {
            label: 'serialize',
            type: 'string',
            op: JSON.stringify,
          },
          {
            label: 'string',
            type: 'string',
            op: () => '',
          },
          {
            label: 'true',
            type: 'boolean',
            op: () => true,
          },
          {
            label: 'false',
            type: 'boolean',
            op: () => false,
          },
          {
            label: 'null',
            type: 'null',
            op: () => null,
          },
        ]
        : t == 'string' ? [
          {
            label: 'to object value',
            type: 'object',
            op: x => ({ '': x }),
          },
          {
            label: 'to object key',
            type: 'object',
            op: this.toObjectKey,
          },
          {
            label: 'object',
            type: 'object',
            op: () => ({}),
          },
          {
            label: 'to array element',
            type: 'array',
            op: x => [x],
          },
          {
            label: 'array',
            type: 'array',
            op: () => [],
          },
          {
            label: 'to int',
            type: 'number',
            op: parseInt,
          },
          {
            label: 'to float',
            type: 'number',
            op: parseFloat,
          },
          {
            label: 'number',
            type: 'number',
            op: () => 0,
          },
          {
            label: 'escape',
            type: 'string',
            op: escape,
          },
          {
            label: 'encode URI',
            type: 'string',
            op: encodeURI,
          },
          {
            label: 'encode URI component',
            type: 'string',
            op: encodeURIComponent,
          },
          {
            label: 'unescape',
            type: 'string',
            op: unescape,
          },
          {
            label: 'decode URI',
            type: 'string',
            op: decodeURI,
          },
          {
            label: 'decode URI component',
            type: 'string',
            op: decodeURIComponent,
          },
          {
            label: 'string',
            type: 'string',
            op: () => '',
          },
          {
            label: 'parse json',
            type: 'unknown',
            op: JSON.parse,
          },
          {
            label: 'true',
            type: 'boolean',
            op: () => true,
          },
          {
            label: 'false',
            type: 'boolean',
            op: () => false,
          },
          {
            label: 'null',
            type: 'null',
            op: () => null,
          },
        ]
        : t == 'boolean' ? [
          {
            label: 'to object value',
            type: 'object',
            op: x => ({ '': x }),
          },
          {
            label: 'to object key',
            type: 'object',
            op: this.toObjectKey,
          },
          {
            label: 'object',
            type: 'object',
            op: () => ({}),
          },
          {
            label: 'to array element',
            type: 'array',
            op: x => [x],
          },
          {
            label: 'array',
            type: 'array',
            op: () => [],
          },
          {
            label: 'number',
            type: 'number',
            op: () => 0,
          },
          {
            label: 'serialize',
            type: 'string',
            op: JSON.stringify,
          },
          {
            label: 'string',
            type: 'string',
            op: () => '',
          },
          this._value === false ? {
            label: 'true',
            type: 'boolean',
            op: () => true,
          }
          : {
            label: 'false',
            type: 'boolean',
            op: () => false,
          },
          {
            label: 'null',
            type: 'null',
            op: () => null,
          },
        ]
        :[
          {
            label: 'to object value',
            type: 'object',
            op: x => ({ '': x }),
          },
          {
            label: 'to object key',
            type: 'object',
            op: this.toObjectKey,
          },
          {
            label: 'object',
            type: 'object',
            op: () => ({}),
          },
          {
            label: 'to array element',
            type: 'array',
            op: x => [x],
          },
          {
            label: 'array',
            type: 'array',
            op: () => [],
          },
          {
            label: 'number',
            type: 'number',
            op: () => 0,
          },
          {
            label: 'serialize',
            type: 'string',
            op: JSON.stringify,
          },
          {
            label: 'string',
            type: 'string',
            op: () => '',
          },
          {
            label: 'true',
            type: 'boolean',
            op: () => true,
          },
          {
            label: 'false',
            type: 'boolean',
            op: () => false,
          },
          {
            label: 'null',
            type: 'null',
            op: () => null,
          },
        ]
      ).filter( x => x.op );
    }
  },
  watch: {
    value( val ) {
      this.updateVal();
    }
  }
}
</script>

<style lang="scss">
.json-widget {
  .json-delim {
    font-weight: bold;
    color: midnightblue;
  }
}
</style>

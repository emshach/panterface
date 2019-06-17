<template lang="html">
  <div>
    <template v-if="editMode">
      <vk-table v-if="field.wip && field.wip.length" responsive hoverable striped 
                class="edit-view" :selected-rows.sync="selected"
                :divided="false" :data="field.wip">
        <vk-col-select/>
        <vk-column v-for="c in columns"
                   :key="c.name" :title="c.name" :cell="c.name">
          <component slot-scope="{ cell }"
                     :is="cell.meta.type" :name="cell.meta.name"
                     :type="cell.meta.type" :field="cell" empty-value="not set" />
        </vk-column>
      </vk-table>
    </template>
    <vk-table v-else-if="isset" responsive hoverable striped
              :divided="false"
              :data="field.value||[]">
      <vk-column v-for="c in columns"
                 :key="c.name" :title="c.name" :cell="c.name">
          <component slot-scope="{ cell }" :readonly="true"
                     :is="cell.meta.type" :name="cell.meta.name"
                     :type="cell.meta.type" :field="cell" empty-value="not set" />
      </vk-column>
    </vk-table>
    <div v-else v-html="html" @click="editField" @focus="editField"
         :class="fieldClasses" />
    <div :class="fieldClasses">
      <template v-if="editMode">
        <label class="uk-flex">
          <span class="uk-margin-right">add</span>
          <multiselect v-model="values" ref="inputV"
                       :options="options"
                       :multiple="true"
                       label="title"
                       track-by="path"
                       open-direction="bottom"
                       @search-change="getObjects"
                       />
          <vk-btn-grp class="uk-align-right">
            <vk-btn-link class="btn btn-confirm" @click.prevent="commit">
              <font-awesome-icon icon="check" /> done
            </vk-btn-link>
            <vk-btn-link class="btn btn-cancel" @click.prevent="cancel">
              <font-awesome-icon icon="times" /> cancel
            </vk-btn-link>
          </vk-btn-grp>
        </label>
      </template>
      <vk-btn-link v-else class="btn btn-add" type="light" size="small"
                   @click="editField" @focus="editField">
        <font-awesome-icon :icon="isset ? 'edit' : 'plus'" />
        add{{ isset? '/edit' : '' }}
      </vk-btn-link>
    </div>
  </div>
</template>

<script lang="js">
import { Field } from '@/lib/objects'
import {
  Table as VkTable,
  TableColumn as VkColumn,
  TableColumnSelect as VkColSelect
} from 'vuikit/lib/table'
import {
  ButtonLink as VkBtnLink,
  ButtonGroup as VkBtnGrp
} from 'vuikit/lib/button'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faTimes,
  faCheck,
  faPlus,
  faEdit
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ModelFieldMixin, ModelModelsFieldMixin } from '@/lib/mixins'
import fields from './'

library.add( faTimes, faCheck, faPlus, faEdit );

VkBtnLink.props.type.validator = val => !val || /^(light|primary|secondary|danger|text|link)$/.test( val );

export default {
  name: 'ModelMultipleChoiceField',
  mixins: [ ModelFieldMixin, ModelModelsFieldMixin ],
  components: {
    VkTable,
    VkColumn,
    VkColSelect,
    VkBtnLink,
    VkBtnGrp,
    FontAwesomeIcon,
    ...fields
  },
  props: {},
  mounted() {
    const m = this.field.meta.related;
    this.related = this.$store.state.models[m];
  },
  data() {
    return {
      related: null,
      selected: [],
    }
  },
  methods: {
    commit() {
      const m = this.field.meta.related;
      let l = this.field.meta.link_field;
      if ( !l ) {
        this.commitField();
        return;
      }
      if ( this.values.length ) {
        const model = this.$store.state.models[m];
        var values = this.values.map( v => {
          var link = { _model: model };
          model.fields.forEach( f => {
            link[ f.name ] = Field(f);
          });
          link[l].value = v;
          return link;
        });
        this.field.wip = ( this.field.wip || [] ).concat( values );
        this.values = [];
        return;
      }
      this.commitField();
    },
    cancel() {
      if ( this.values.length ) {
          this.values = [];
        return;
      }
      this.revertField();
    }
  },
  computed: {
    columns() {
      return this.related ? this.related.fields : [];
    },
    searchModel() {
      let l = this.field.meta.link_field;
      if (l) {
        const model = this.related;
        var f = model && model.fields.find( x => x.name === l );
        return f && f.related;
      }
      return this.field.meta.related;
    }
  }
}
</script>

<style lang="scss">
.model-multiple-choice-field {
  .btn {
    padding: 0 7px;
    height: 30px;
    line-height: 33px;
  }
  .uk-table {
    th {
      font-size: 12px;
      padding: 2px 12px;
    }
    td {
      font-size: 14px;
      padding: 4px 12px;
    }
    &.uk-table-striped {
      > tr:nth-of-type(odd), tbody tr:nth-of-type(odd) {
        background: rgba(0,0,0,0.02);
        border-top: 1px solid rgba(0,0,0,0.08);
        border-bottom: 1px solid rgba(0,0,0,0.10);
        &.uk-active {
          background: #ffb;
        }
      }
    }
    &.uk-table-hover {
      > tr:nth-of-type(odd), tbody tr:nth-of-type(odd) {
        &:hover {
          background: #ffb;
        }
      }
    }
  }
}
</style>

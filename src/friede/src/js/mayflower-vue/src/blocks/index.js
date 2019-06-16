export const Centerfold = () =>
   import(/* webpackChunkName: "blocks" */ './Centerfold')
export const ListDisplay = () =>
   import(/* webpackChunkName: "blocks" */ './ListDisplay')
export const GridDisplay = () =>
   import(/* webpackChunkName: "blocks" */ './GridDisplay')
export const FilterList = () =>
   import(/* webpackChunkName: "blocks" */ './FilterList')
export const FilterGrid = () =>
   import(/* webpackChunkName: "blocks" */ './FilterGrid')

export default {
  Centerfold,
  ListDisplay,
  GridDisplay,
  FilterList,
  FilterGrid,
}


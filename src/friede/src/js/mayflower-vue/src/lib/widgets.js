const DashboardWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/DashboardWidget' )
const InlineWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/InlineWidget' )
const AdaptiveWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/AdaptiveWidget' )
const ViewModelWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/ViewModelWidget' )
// const ListModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/ListModelWidget' )
// const NewModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/NewModelWidget' )
// const EditModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/EditModelWidget' )
// const ReportModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/ReportModelWidget' )
// const ModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/ModelWidget' )
// const AddModelWidget = () =>
//         import/* webpackChunkName: "widgets" */( '@/components/AddModelWidget' )
// const RemoveModelWidget = () =>
//         import/* webpackChunkName: "widgets" */( '@/components/RemoveModelWidget' )
const Widget = () => import(/* webpackChunkName: "widgets" */ '@/components/Widget' )

export {
  DashboardWidget,
  InlineWidget,
  AdaptiveWidget,
  ViewModelWidget,
  // ListModelWidget,
  // NewModelWidget,
  // EditModelWidget,
  // ReportModelWidget,
  // ModelWidget,
  // AddModelWidget,
  // RemoveModelWidget,
  Widget
}
export default {
  DashboardWidget,
  InlineWidget,
  AdaptiveWidget,
  ViewModelWidget,
  // ListModelWidget,
  // NewModelWidget,
  // EditModelWidget,
  // ReportModelWidget,
  // ModelWidget,
  // AddModelWidget,
  // RemoveModelWidget,
  Widget
}

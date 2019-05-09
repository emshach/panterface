const DashboardWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/wx/DashboardWidget' )
const InlineWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/wx/InlineWidget' )
const AdaptiveWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/wx/AdaptiveWidget' )
const ViewModelWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/wx/ViewModelWidget' )
// const ListModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/wx/ListModelWidget' )
// const NewModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/wx/NewModelWidget' )
// const EditModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/wx/EditModelWidget' )
// const ReportModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/wx/ReportModelWidget' )
// const ModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/wx/ModelWidget' )
// const AddModelWidget = () =>
//         import/* webpackChunkName: "widgets" */( '@/components/wx/AddModelWidget' )
// const RemoveModelWidget = () =>
//         import/* webpackChunkName: "widgets" */( '@/components/wx/RemoveModelWidget' )
const Widget = () => import(/* webpackChunkName: "widgets" */ '@/components/wx/Widget' )

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

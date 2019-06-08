export const DashboardWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/wx/DashboardWidget' )
export const InlineWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/wx/InlineWidget' )
export const AdaptiveWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/wx/AdaptiveWidget' )
export const ViewModelWidget = () =>
        import(/* webpackChunkName: "widgets" */ '@/components/wx/ViewModelWidget' )
// export const ListModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/wx/ListModelWidget' )
// export const NewModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/wx/NewModelWidget' )
// export const EditModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/wx/EditModelWidget' )
// export const ReportModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/wx/ReportModelWidget' )
// export const ModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ '@/components/wx/ModelWidget' )
// export const AddModelWidget = () =>
//         import/* webpackChunkName: "widgets" */( '@/components/wx/AddModelWidget' )
// export const RemoveModelWidget = () =>
//         import/* webpackChunkName: "widgets" */( '@/components/wx/RemoveModelWidget' )
export const Widget = () =>
   import(/* webpackChunkName: "widgets" */ '@/components/wx/Widget' )

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

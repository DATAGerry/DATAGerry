import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {SearchComponent} from "./search.component";
import {NavigationComponent} from "../layout/components/navigation/navigation.component";
import {SidebarComponent} from "../layout/components/sidebar/sidebar.component";
import {BreadcrumbComponent} from "../layout/components/breadcrumb/breadcrumb.component";
import {TextSearchComponent} from "./components/text-search/text-search.component";

const routes: Routes = [
  {
    path: '',
    component: NavigationComponent,
    outlet: 'navigation'
  },
  {
    path: '',
    component: SidebarComponent,
    outlet: 'sidebar'
  },
  {
    path: '',
    component: BreadcrumbComponent,
    outlet: 'breadcrumb'
  },
  {
    path: '',
    component: SearchComponent
  },
  {
    path: 'text',
    component: TextSearchComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SearchRoutingModule { }

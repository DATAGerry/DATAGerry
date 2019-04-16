import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FooterComponent } from './components/footer/footer.component';
import { NavigationComponent } from './components/navigation/navigation.component';
import { RouterModule } from '@angular/router';
import { BreadcrumbComponent } from './components/breadcrumb/breadcrumb.component';
import { BreadcrumbService } from './components/breadcrumb/breadcrumb.service';
import { SidebarComponent } from './components/sidebar/sidebar.component';
import { SidebarCategoryComponent } from './components/sidebar/sidebar-category.component';

@NgModule({
  declarations: [
    BreadcrumbComponent,
    NavigationComponent,
    FooterComponent,
    SidebarComponent,
    SidebarCategoryComponent
  ],
  exports: [
    NavigationComponent,
    BreadcrumbComponent,
    FooterComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ],
  providers: [
    BreadcrumbService
  ]
})
export class LayoutModule {
}

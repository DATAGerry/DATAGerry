import { Component, OnDestroy, OnInit, Renderer2 } from '@angular/core';
import { ApiCallService } from '../../../services/api-call.service';

@Component({
  selector: 'cmdb-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit, OnDestroy {
  public categoryTree: any;
  constructor(private api: ApiCallService, private renderer: Renderer2) { }

  public ngOnInit(): void {
    this.renderer.addClass(document.body, 'sidebar-fixed');
    const categoryTreeObserver = this.api.callGetRoute('category/tree');
    categoryTreeObserver.subscribe(tree => {
      this.categoryTree = tree;
    });
  }

  public ngOnDestroy(): void {
    this.renderer.removeClass(document.body, 'sidebar-fixed');
  }

}

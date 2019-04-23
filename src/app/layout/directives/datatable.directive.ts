import { Directive, ElementRef, Input, OnDestroy, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import 'datatables.net';

@Directive({
  selector: '[cmdbDatatable]'
})
export class DatatableDirective implements OnInit, OnDestroy {

  @Input()
  dtOptions: DataTables.Settings = {};

  @Input()
  dtTrigger: Subject<any>;

  dtInstance: Promise<DataTables.Api>;

  private dt: DataTables.Api;

  constructor(private el: ElementRef) {
  }

  public ngOnDestroy(): void {
    if (this.dtTrigger) {
      this.dtTrigger.unsubscribe();
    }
  }

  public ngOnInit(): void {
    if (this.dtTrigger) {
      this.dtTrigger.subscribe(() => {
        this.displayTable();
      });
    } else {
      this.displayTable();
    }
  }

  private displayTable(): void {
    this.dtInstance = new Promise((resolve, reject) => {
      Promise.resolve(this.dtOptions).then(dtOptions => {
        setTimeout(() => {
          this.dt = $(this.el.nativeElement).DataTable(dtOptions);
          resolve(this.dt);
        });
      });
    });
  }

}

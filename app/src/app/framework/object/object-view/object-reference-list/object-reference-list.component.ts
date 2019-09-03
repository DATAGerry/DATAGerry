import { Component, Input, OnDestroy, ViewChild } from '@angular/core';
import { Subject } from 'rxjs';
import { RenderResult } from '../../../models/cmdb-render';
import { ObjectService } from '../../../services/object.service';
import { DataTableDirective } from 'angular-datatables';

@Component({
  selector: 'cmdb-object-reference-list',
  templateUrl: './object-reference-list.component.html',
  styleUrls: ['./object-reference-list.component.scss']
})
export class ObjectReferenceListComponent implements OnDestroy {

  private id: number;

  @ViewChild(DataTableDirective, {static: true})
  private dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  public referenceList: RenderResult[] = [];

  @Input()
  set publicID(publicID: number) {
    this.id = publicID;
    if (this.id !== undefined && this.id !== null) {
      this.loadObjectReferences();
    }
  }

  get publicID(): number {
    return this.id;
  }

  public constructor(private objectService: ObjectService) {
  }

  private loadObjectReferences() {
    this.objectService.getObjectReferences(this.publicID).subscribe((references: RenderResult[]) => {
        this.referenceList = references;
      },
      (error) => {
        console.error(error);
      },
      () => {
        this.renderTable();
      });
  }

  private renderTable(): void {
    if (this.dtElement.dtInstance === undefined) {
      this.dtTrigger.next();
    } else {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        dtInstance.destroy();
        this.dtTrigger.next();
      });
    }

  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }
}

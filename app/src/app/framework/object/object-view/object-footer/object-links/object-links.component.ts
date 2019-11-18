import { Component, Input, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { LinkService } from '../../../../services/link.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbLink } from '../../../../models/cmdb-link';
import { Subject, Subscription } from 'rxjs';
import { DataTableDirective } from 'angular-datatables';
import { RenderResult } from '../../../../models/cmdb-render';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ObjectLinkAddModalComponent } from '../../../components/modals/object-link-add-modal/object-link-add-modal.component';

@Component({
  selector: 'cmdb-object-links',
  templateUrl: './object-links.component.html',
  styleUrls: ['./object-links.component.scss']
})
export class ObjectLinksComponent implements OnInit, OnDestroy {

  // Data
  private id: number;

  @Input()
  set publicID(publicID: number) {
    this.id = publicID;
    if (this.id !== undefined && this.id !== null) {
      this.loadLinks();
    }
  }

  get publicID(): number {
    return this.id;
  }

  @Input() public renderResult: RenderResult = undefined;
  public linkList: CmdbLink[];
  private linkListSubscription: Subscription;

  // Table
  @ViewChild(DataTableDirective, { static: true })
  private dtElement: DataTableDirective;
  public readonly dtOptions: any = {
    ordering: true,
    order: [[3, 'asc']],
    language: {
      search: '',
      searchPlaceholder: 'Filter...'
    }
  };
  public dtTrigger: Subject<any>;

  constructor(private linkService: LinkService, private modalService: NgbModal) {
    this.linkList = [];
  }

  public ngOnInit(): void {
    this.dtTrigger = new Subject();
    this.linkListSubscription = new Subscription();
  }

  public onShowAddModal(): void {
    const modalRef = this.modalService.open(ObjectLinkAddModalComponent);
    modalRef.componentInstance.renderResult = this.renderResult;
  }

  private loadLinks(): void {
    this.linkService.getLinks(this.publicID).subscribe(
      (resp: CmdbLink[]) => this.linkList = resp,
      (error) => console.error(error),
      () => this.renderTable()
    );
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
    this.linkListSubscription.unsubscribe();
    this.dtTrigger.unsubscribe();
  }
}

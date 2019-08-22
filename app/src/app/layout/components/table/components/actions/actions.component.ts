import {Component, Input} from '@angular/core';
import {TableColumnAction} from '../../models/table-columns-action';
import {ApiCallService} from '../../../../../services/api-call.service';
import {ActivatedRoute, Router} from '@angular/router';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';
import {ModalComponent} from '../../../../helpers/modal/modal.component';

@Component({
  selector: 'cmdb-actions',
  templateUrl: './actions.component.html',
  styleUrls: ['./actions.component.scss']
})
export class ActionsComponent {

  @Input() data: TableColumnAction[];
  @Input() publicID: string = '';

  constructor(private apiCallService: ApiCallService, private modalService: NgbModal,
              private activeRoute: ActivatedRoute, private router: Router) {
  }

  public delObject(route: any) {
    if ( route === 'delete/') {
      this.router.navigate([this.router.url + '/' + route + this.publicID]);
    }

    if ( route === 'object/') {
      const modalComponent = this.modalService.open(ModalComponent);
      modalComponent.componentInstance.modalMessage = 'Are you sure you want to delete this Object? test';
      modalComponent.result.then((result) => {
        if (result) {
          this.apiCallService.callDeleteRoute(route + this.publicID).subscribe(data => {
            const forwardingUrl = '/framework/' + route;
            this.router.navigate([forwardingUrl]);
          });
        }
      });
    }
  }

}

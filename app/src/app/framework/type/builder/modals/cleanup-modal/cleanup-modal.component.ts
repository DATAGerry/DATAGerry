import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {NgbActiveModal, NgbModal} from '@ng-bootstrap/ng-bootstrap';
import {CmdbType} from '../../../../models/cmdb-type';
import {TypeService} from '../../../../services/type.service';
import {UserService} from '../../../../../management/services/user.service';

@Component({
  selector: 'cmdb-cleanup-modal',
  templateUrl: './cleanup-modal.component.html',
  styleUrls: ['./cleanup-modal.component.scss']
})
export class CleanupModalComponent implements OnInit {

  @Input() typeInstance: CmdbType = null;
  public remove: boolean = false;
  public update: boolean = false;

  constructor( private typeService: TypeService, public userService: UserService, public activeModal: NgbActiveModal) {
  }

  ngOnInit() {
    if (this.typeInstance.clean_db === false) {
      this.typeService.cleanupRemovedFields(this.typeInstance.public_id).subscribe(() => {
          this.remove = true;
        }, error => {console.log(error); },
        () => {
          this.typeService.cleanupInsertedFields(this.typeInstance.public_id).subscribe(() => {
              this.update = true;
            }, error => console.log(error),
            () => {
              if (this.remove && this.update) {
                this.typeInstance.clean_db = true;
                this.typeService.putType(this.typeInstance).subscribe(() => {
                  console.log('ok');
                });
              }
            });
        });
    }
  }
}

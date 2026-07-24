/**
 * G3 stub — port vào ART-ERP-FE-CRM khi có quyền push submodule.
 * Form code: opportunity · Mock data, không gọi API.
 */
import { Component } from '@angular/core';
import { NavController, ModalController, AlertController, LoadingController, PopoverController } from '@ionic/angular';
import { EnvService } from 'src/app/services/core/env.service';
import { PageBase } from 'src/app/page-base';
import { Location } from '@angular/common';

@Component({
	selector: 'app-opportunity',
	templateUrl: 'opportunity.page.html',
	styleUrls: ['opportunity.page.scss'],
	standalone: false,
})
export class OpportunityPage extends PageBase {
	constructor(
		public modalController: ModalController,
		public popoverCtrl: PopoverController,
		public alertCtrl: AlertController,
		public loadingController: LoadingController,
		public env: EnvService,
		public navCtrl: NavController,
		public location: Location
	) {
		super();
		this.pageConfig.pageName = 'opportunity';
		this.pageConfig.pageTitle = 'Opportunity';
	}

	preLoadData(event?: any): void {
		this.items = [
			{ Id: 1001, Name: 'Tiệc cưới Nguyễn & Trần', Stage: 'Tour', EventDate: '2026-12-20', NumberOfGuests: 300, Hall: 'Diamond', Owner: 'Sale A', Amount: 450000000 },
			{ Id: 1002, Name: 'Year-end ABC', Stage: 'Quote', EventDate: '2026-12-28', NumberOfGuests: 150, Hall: 'Ruby', Owner: 'Sale B', Amount: 180000000 },
		];
		this.pageConfig.showSpinner = false;
		this.loadedData(event);
	}
}

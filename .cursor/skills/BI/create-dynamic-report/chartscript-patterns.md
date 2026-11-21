# ChartScript patterns (ART Dynamic Report)

Copy and adapt. Always re-read live script via `report_get` before overwrite.

## Pie + status color + translate + center total + mini

Parent status code: `ShipmentStatus` or `SalesOrder`.

```js
option.series = Array.isArray(option.series) ? option.series : (option.series ? [option.series] : []);
option.series.forEach(function (s) {
	s.type = 'pie';
	s.radius = s.radius || ['45%', '60%'];
	s.center = s.center || ['50%', '50%'];
});
if (option.xAxis) option.xAxis = undefined;
if (option.yAxis) option.yAxis = undefined;
option.tooltip = option.tooltip || {};
option.tooltip.trigger = 'item';

var isMini = this.viewMode === 'mini';
var chart = this.chart;
var env = this.env;

function finishPie() {
	var total = 0;
	option.series.forEach(function (s) {
		if (!s.data || !Array.isArray(s.data)) return;
		s.data.forEach(function (d) { total += +d.value || 0; });
	});
	var dark = (li && li.chartTextColor) ? li.chartTextColor() : '';
	option.title = undefined;
	option.graphic = [{
		type: 'text',
		left: 'center',
		top: 'center',
		z: 100,
		style: {
			text: String(total),
			textAlign: 'center',
			textVerticalAlign: 'middle',
			fontSize: isMini ? 16 : 28,
			fontWeight: 'bold',
			fill: dark
		}
	}];
	if (isMini) {
		option.legend = { show: false };
		option.toolbox = { show: false };
		option.series.forEach(function (s) {
			s.label = { show: false };
			s.labelLine = { show: false };
			s.radius = ['72%', '88%'];
			s.center = ['50%', '50%'];
		});
	}
	if (chart) chart.setOption(option, true);
}

function applyStatusList(list) {
	var seriesArr = Array.isArray(option.series) ? option.series : [option.series];
	var tasks = [];
	seriesArr.forEach(function (s) {
		if (!s || !s.data || !Array.isArray(s.data)) return;
		s.data.forEach(function (item) {
			if (!item || item.name == null) return;
			var row = li.findStatusInList(list, item.name);
			if (!row) return;
			var css = li.resolveIonColorCss(row.Color || row.BadgeColor);
			if (css) item.itemStyle = Object.assign({}, item.itemStyle || {}, { color: css });
			var key = row.Name || row.Code;
			if (!key || !env || !env.translateResource) return;
			tasks.push(env.translateResource(key).then(function (t) { item.name = t; }));
		});
	});
	return Promise.all(tasks);
}

if (env && env.getStatus) {
	env.getStatus('ShipmentStatus').then(applyStatusList).then(finishPie).catch(finishPie);
} else {
	finishPie();
}
```

## Stacked bar + status series color/translate + tooltip Total

```js
if (option.series && option.series.length)
	option.series.forEach(function (i) { i.stack = 'total'; });

var isMini = this.viewMode === 'mini';
var chart = this.chart;
var env = this.env;
var totalLabel = 'Total';

function finishBar() {
	option.tooltip = option.tooltip || {};
	option.tooltip.trigger = 'axis';
	option.tooltip.axisPointer = option.tooltip.axisPointer || { type: 'shadow' };
	option.tooltip.formatter = function (params) {
		if (!params || !params.length) return '';
		var sum = 0;
		var rows = '';
		params.slice().reverse().forEach(function (param) {
			var value = +param.value || 0;
			if (value === 0) return;
			sum += value;
			rows +=
				'<tr><td>' +
				param.marker +
				'</td><td>' +
				param.seriesName +
				'</td><td class="e-value">' +
				(li && li.currencyFormatFriendly ? li.currencyFormatFriendly(value) : value) +
				'</td></tr>';
		});
		rows +=
			'<tr><td></td><td class="bold">' +
			totalLabel +
			'</td><td class="e-value bold">' +
			(li && li.currencyFormatFriendly ? li.currencyFormatFriendly(sum) : sum) +
			'</td></tr>';
		return (
			'<div class="e-tooltip"><span class="bold">' +
			params[0].axisValueLabel +
			'</span><br/><table class="w-full">' +
			rows +
			'</table></div>'
		);
	};

	if (isMini) {
		option.legend = option.legend || {};
		option.legend.show = false;
		if (option.toolbox) option.toolbox.show = false;
		option.tooltip.show = false;
		if (option.grid) {
			var grids = Array.isArray(option.grid) ? option.grid : [option.grid];
			grids.forEach(function (g) {
				if (!g) return;
				g.top = 4; g.right = 4; g.bottom = 4; g.left = 4; g.containLabel = true;
			});
		}
	}
	if (chart) chart.setOption(option, true);
}

function applyStatusList(list) {
	var seriesArr = Array.isArray(option.series) ? option.series : [option.series];
	var tasks = [];
	seriesArr.forEach(function (s) {
		if (!s || s.name == null || s.name === '') return;
		var row = li.findStatusInList(list, s.name);
		if (!row) return;
		var css = li.resolveIonColorCss(row.Color || row.BadgeColor);
		if (css) s.itemStyle = Object.assign({}, s.itemStyle || {}, { color: css });
		var key = row.Name || row.Code;
		if (!key || !env || !env.translateResource) return;
		tasks.push(env.translateResource(key).then(function (t) { s.name = t; }));
	});
	return Promise.all(tasks);
}

var boot = Promise.resolve();
if (env && env.translateResource) {
	boot = env.translateResource('Total').then(function (t) {
		if (t) totalLabel = t;
	});
}

if (env && env.getStatus) {
	boot
		.then(function () { return env.getStatus('SalesOrder'); })
		.then(applyStatusList)
		.then(finishBar)
		.catch(finishBar);
} else {
	boot.then(finishBar).catch(finishBar);
}
```

## SYS_Status.Name + i18n

- `Name` = English translate key (sentence or unique phrase).
- `vi-VN[Name]` = **exact** old Vietnamese label users saw.
- If two parents need different VI for the same Code, use **different** `Name` keys (example: SalesOrder `In carrier` vs ShipmentStatus `Delivered to carrier`).
- Do not reuse generic keys (`Debt` → Công nợ in payment UI) for status-specific wording — pick a dedicated Name (`Outstanding debt` → Còn nợ).

## Reference report Ids (art / typical)

| Id | Pattern |
| --- | --- |
| 28 | Shipment status pie + mini thin ring + center total |
| 33 / 38 | Same pie family |
| 3 | SO weekly stacked status bar + tooltip Total |
| 5 | Gauge + mini compact |

Live scripts may drift — always `report_get` before copy.

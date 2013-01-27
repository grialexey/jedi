define(
    [
        'momentjs'
    ],
    function(moment) {

    moment.lang('ru');
    moment.relativeTime.s = "минуту";
    moment.calendar = {
        lastDay : 'Вчера в LT',
        sameDay : 'Сегодня в LT',
        nextDay : 'Завтра в LT',
        lastWeek : 'L',
        nextWeek : 'L',
        sameElse : 'L'
    };

    return {
		ENTER_KEY: 13,
		ESC_KEY: 27,
        moment: moment
	};
});
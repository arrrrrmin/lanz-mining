
import { formatDefaultLocale } from "d3-format";
import { timeFormat, timeFormatDefaultLocale } from "d3-time-format";
import {
    timeSecond,
    timeMinute,
    timeHour,
    timeDay,
    timeMonth,
    timeWeek,
    timeYear,
} from "d3-time";

// set default locale
export const formatDeLocale = formatDefaultLocale({
    "decimal": ",",
    "thousands": ".",
    "grouping": [3],
    //"currency": ["", "\u00a0€"]
    "currency": ["", "€"]
});


// set default time locale
export const timeFormatDeLocale = timeFormatDefaultLocale({
    "dateTime": "%A, der %e. %B %Y, %X",
    "date": "%d.%m.%Y",
    "time": "%H:%M:%S",
    "periods": ["AM", "PM"],
    "days": ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
    "shortDays": ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"],
    "months": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
    "shortMonths": ["Jan", "Feb", "Mrz", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
});

let formatMillisecond = timeFormat(".%L");
let formatSecond = timeFormat(":%S");
let formatMinute = timeFormat("%I:%M");
let formatHour = timeFormat("%I %p");
let formatDay = timeFormat("%a %d");
let formatWeek = timeFormat("%b %d");
let formatMonth = timeFormat("%B");
let formatYear = timeFormat("%Y");

export function tickFormat(date) {
    function multiFormat(date) {
        return (timeSecond(date) < date ? formatMillisecond
            : timeMinute(date) < date ? formatSecond
                : timeHour(date) < date ? formatMinute
                    : timeDay(date) < date ? formatHour
                        : timeMonth(date) < date ? (timeWeek(date) < date ? formatDay : formatWeek)
                            : timeYear(date) < date ? formatMonth
                                : formatYear)(date);
    }
    return multiFormat(date);
}

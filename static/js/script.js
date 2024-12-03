 // カードリストと解答エリアの要素を取得
var cardContainer = document.getElementById('card-container');
var answerArea = document.getElementById('answer-box');

// Sortable.jsを使って、ドラッグ＆ドロップを有効化
var sortableCardContainer = Sortable.create(cardContainer, {
    group: "shared", // カードと解答欄を共有グループに設定
    animation: 150,
    sort: false // カードリストの順序は固定
});

var sortableAnswerArea = Sortable.create(answerArea, {
    group: "shared", // 同じグループ名で相互ドラッグ可能に
    animation: 150,
    sort: true // 解答欄内で順序を変更可能
});

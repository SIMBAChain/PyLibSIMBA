pragma solidity ^0.4.24;

contract Application {
    function Application() public {}
    enum Assets {
        complexWidget
    }
    Assets _complexEvent = Assets.complexWidget;

    function complexEvent (
        string assetId, /* parameter needed for linking assets and transactions */
        string aString, /* optional parameter */
        bytes32 someBytes, /* optional parameter */
        byte aByte, /* optional parameter */
        uint aUint, /* optional parameter */
        address anAddress, /* optional parameter */
        int256 anInt, /* optional parameter */
        bool aBool, /* optional parameter */
        string _bundleHash)   /* optional parameter */
    public {}
}
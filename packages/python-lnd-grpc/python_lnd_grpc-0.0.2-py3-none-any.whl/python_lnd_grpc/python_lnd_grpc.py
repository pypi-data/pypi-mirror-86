# python3
import os
import binascii
import codecs
import grpc
from python_lnd_grpc.lnd_defaults import defaultTLSCertFilename, defaultAdminMacFilename, defaultNetwork, defaultRPCHost, defaultRPCPort
# from . import rpc_pb2, rpc_pb2_grpc
import python_lnd_grpc.protos.rpc_pb2 as lnrpc
import python_lnd_grpc.protos.rpc_pb2_grpc as rpcstub

# lnrpc = rpc_pb2
# rpcstub = rpc_pb2_grpc
# TODO: path for for system other than linux
TLS_FILE = os.path.expanduser('~/.lnd/' + defaultTLSCertFilename)
ADMIN_MACAROON_PATH = '~/.lnd/data/chain/bitcoin/'


class Connector(object):
    def __init__(
        self,
        tls_file: str = TLS_FILE,
        macaroon_path: str = ADMIN_MACAROON_PATH,
        macaroon_filename: str = defaultAdminMacFilename,
        network: str = defaultNetwork,
        grpc_host: str = defaultRPCHost,
        grpc_port: str = defaultRPCPort):

        self.full_macaroon_path = os.path.expanduser((macaroon_path + '{}/' + macaroon_filename).format(network))
        with open(TLS_FILE, 'rb') as f:
            self.cert = f.read()
        with open(self.full_macaroon_path, 'rb') as f:
            self.macaroon_bytes = f.read()
            self.macaroon = codecs.encode(self.macaroon_bytes, 'hex')
        self.headers = {'Grpc-Metadata-macaroon': self.macaroon}

    @property
    def _ln_stub(self):
        channel = grpc.secure_channel((defaultRPCHost + ":" + defaultRPCPort), self.combined_credentials)
        return rpcstub.LightningStub(channel)

    @property
    def combined_credentials(self) -> grpc.CallCredentials:
        ssl_creds = grpc.ssl_channel_credentials(self.cert)
        auth_creds = grpc.metadata_call_credentials(self.auth_metadata_plugin)
        return grpc.composite_channel_credentials(ssl_creds, auth_creds)

    def auth_metadata_plugin(self, _, callback):
        callback([("macaroon", self.macaroon)], None)

class LNDMethods(Connector):
    # https://api.lightning.community/#abandonchannel
    def abandon_channel(self, chan_point):
        request = lnrpc.AbandonChannelRequest(
            channel_point = chan_point,
        )
        response = self._ln_stub.AbandonChannel(request)
        return response

    # https://api.lightning.community/#closechannel
    def close_channel(self, channel_point, force: bool, target_conf: int, sat_per_byte: int, delivery_address: str):
        request = lnrpc.CloseChannelRequest(
            channel_point=channel_point,
            force=force,
            target_conf=target_conf,
            sat_per_byte=sat_per_byte,
            delivery_address=delivery_address,
        )
        response = self._ln_stub.CloseChannel(request)
        return response

    # https://api.lightning.community/#channelbalance
    def channel_balance(self):
        response = self._ln_stub.ChannelBalance(lnrpc.ChannelBalanceRequest())
        return response
    
    # https://api.lightning.community/#connectpeer
    def connect_peer(self, pubkey: str, host: str, perm: bool = False):
        #async when perm = True
        address = lnrpc.LightningAddress(pubkey=pubkey, host=host)
        request = lnrpc.ConnectPeerRequest(addr = address, perm = perm)
        response = self._ln_stub.ConnectPeer(request)
        return response

    # https://api.lightning.community/#decodepayreq
    def decode_pay_req(self, pay_request: str):
        request = lnrpc.PayReqString(
            pub_key=pay_request,
        )
        response = self._ln_stub.DecodePayReq(request)
        return response

    # https://api.lightning.community/#describegraph
    def describe_graph(self, unannounced: bool):
        request = lnrpc.ChannelGraphRequest(
            include_unannounced=unannounced,
        )
        response = self._ln_stub.DescribeGraph(request)
        return response

    # https://api.lightning.community/#disconnectpeer
    def disconnect_peer(self, pubkey: str):
        request = lnrpc.DisconnectPeerRequest(
            pub_key=pubkey,
        )
        response = self._ln_stub.DisconnectPeer(request)
        return response

    # https://api.lightning.community/#estimatefee
    def estimate_fee(self, addr_to_amount, target_confirmed: int):
        request = lnrpc.EstimateFeeRequest(
            AddrToAmount=addr_to_amount,
            target_conf=target_confirmed,
        )
        response = self._ln_stub.EstimateFee(request)
        return response

    # https://api.lightning.community/#feereport
    def fee_report(self):
        response = self._ln_stub.FeeReport(lnrpc.FeeReportRequest())
        return response

     # https://api.lightning.community/#getchaninfo
    def get_chan_info(self, chanid: int):
        request = lnrpc.ChanInfoRequest(
            chan_id=chanid,
        )
        response = self._ln_stub.GetChanInfo(request)
        return response

    # https://api.lightning.community/#getinfo
    def get_info(self):
        response = self._ln_stub.GetInfo(lnrpc.GetInfoRequest())
        return response

    # https://api.lightning.community/#getnetworkinfo
    def get_network_info(self):
        response = self._ln_stub.GetNetworkInfo(lnrpc.NetworkInfoRequest())
        return response

    # https://api.lightning.community/#getnodeinfo
    def get_node_info(self, pubkey: str, include: bool):
        request = lnrpc.NodeInfoRequest(
            pub_key=pubkey,
            include_channels=include,
        )
        response = self._ln_stub.GetNodeInfo(request)
        return response

    # https://api.lightning.community/#getrecoveryinfo
    def get_recovery_info(self):
        response = self._ln_stub.GetRecoveryInfo(lnrpc.GetRecoveryInfoRequest())
        return response

    # https://api.lightning.community/#gettransactions
    def get_transactions(self, start_height: int, end_height: int):
        request = lnrpc.GetTransactionsRequest(
            start_height=start_height,
            end_height=end_height,
        )
        response = self._ln_stub.GetTransactions(request)
        return response

    # https://api.lightning.community/#listchannels
    def list_channels(self, active: bool, inactive: bool, public: bool, private: bool, peer: bytes):
        request = lnrpc.ListChannelsRequest(
            active_only=active,
            inactive_only=inactive,
            public_only=public,
            private_only=private,
            peer=peer,
        )
        response = self._ln_stub.ListChannels(request)
        return response

    # https://api.lightning.community/#listinvoices
    def list_invoices(self, pending_only: bool, offset: int, max_invoices: int, reverse: bool):
        request = lnrpc.ListInvoiceRequest(
            pending_only=pending_only,
            index_offset=offset,
            num_max_invoices=max_invoices,
            reversed=reverse,
        )
        response = self._ln_stub.ListInvoices(request)
        return response

    # https://api.lightning.community/#listpayments
    def list_payments(self, incomplete: bool, offset: int, max_payments: int, reverse: bool):
        request = lnrpc.ListPaymentsRequest(
            include_incomplete=incomplete,
            index_offset=offset,
            max_payments=max_payments,
            reversed=reverse,
        )
        response = self._ln_stub.ListPayments(request)
        return response

    # https://api.lightning.community/#listpeers
    def list_peers(self, latest_error: bool):
        request = lnrpc.ListPeersRequest(
            latest_error=latest_error,
        )
        response = self._ln_stub.ListPeers(request)
        return response

    # https://api.lightning.community/#listunspent
    def list_unspent(self, min_confs: int, max_confs: int):
        request = lnrpc.ListUnspentRequest(
            min_confs=min_confs,
            max_confs=max_confs,
        )
        response = self.stub.ListUnspent(request)
        return response

    # https://api.lightning.community/#lookupinvoice
    def lookup_invoice(self, r_hash_str: str, r_hash: bool):
        request = lnrpc.PaymentHash(
            r_hash_str=r_hash_str,
            r_hash=r_hash,
        )
        response = self._ln_stub.LookupInvoice(request)
        return response

    # https://api.lightning.community/#newaddress
    def new_address(self):
        response = self._ln_stub.NewAddress(lnrpc.NewAddressRequest())
        return response

    # https://api.lightning.community/#openchannel
    def open_channel(
        self, 
        node_pubkey: bytes,
        node_pubkey_string: str,
        local_funding_amount: int,
        push_sat: int,
        target_conf: int,
        sat_per_byte: int,
        private: bool,
        min_htlc_msat: int,
        remote_csv_delay: int,
        min_confs: int,
        spend_unconfirmed: bool,
        close_address: str,
        fundingShim,
        remote_max_value_in_flight_msat: int):
        request = lnrpc.OpenChannelRequest(
            node_pubkey=node_pubkey,
            node_pubkey_string=node_pubkey_string,
            local_funding_amount=local_funding_amount,
            push_sat=push_sat,
            target_conf=target_conf,
            sat_per_byte=sat_per_byte,
            private=private,
            min_htlc_msat=min_htlc_msat,
            remote_csv_delay=remote_csv_delay,
            min_confs=min_confs,
            spend_unconfirmed=spend_unconfirmed,
            close_address=close_address,
            funding_shim=funding_shim,
            remote_max_value_in_flight_msat=remote_max_value_in_flight_msat,
        )
        response = self._ln_stub.OpenChannel(request)
        return response

    # https://api.lightning.community/#openchannelsync
    def open_channel_sync(
        self, 
        node_pubkey: bytes,
        node_pubkey_string: str,
        local_funding_amount: int,
        push_sat: int,
        target_conf: int,
        sat_per_byte: int,
        private: bool,
        min_htlc_msat: int,
        remote_csv_delay: int,
        min_confs: int,
        spend_unconfirmed: bool,
        close_address: str,
        fundingShim,
        remote_max_value_in_flight_msat: int):
        request = lnrpc.OpenChannelRequest(
            node_pubkey=node_pubkey,
            node_pubkey_string=node_pubkey_string,
            local_funding_amount=local_funding_amount,
            push_sat=push_sat,
            target_conf=target_conf,
            sat_per_byte=sat_per_byte,
            private=private,
            min_htlc_msat=min_htlc_msat,
            remote_csv_delay=remote_csv_delay,
            min_confs=min_confs,
            spend_unconfirmed=spend_unconfirmed,
            close_address=close_address,
            funding_shim=funding_shim,
            remote_max_value_in_flight_msat=remote_max_value_in_flight_msat,
        )
        response = self._ln_stub.OpenChannelSync(request)
        return response

    # https://api.lightning.community/#pendingchannels
    def pending_channels(self):
        response = self._ln_stub.PendingChannels(lnrpc.PendingChannelsRequest())
        return response

    # https://api.lightning.community/#restorechannelbackups
    def restore_channel_backups(self, chan_backups, multi_chan_backup: bytes):
        request = lnrpc.RestoreChanBackupRequest(
            chan_backups=chan_backups,
            multi_chan_backup=multi_chan_backup,
        )
        response = self._ln_stub.RestoreChannelBackups(request)
        return response

    # https://api.lightning.community/#sendcoins
    def send_coins(self, addr: str, amount: int, target_conf: int, sat_per_byte: int, send_all: bool, label: str):
        request = lnrpc.SendCoinsRequest(
            addr=addr,
            amount=amount,
            target_conf=target_conf,
            sat_per_byte=sat_per_byte,
            send_all=send_all,
            label=label,
        )
        response = self._ln_stub.SendCoins(request)
        return response

    # https://api.lightning.community/#sendmany
    def send_many(self, AddrToAmount, target_conf: int, sat_per_byte: int, label: str):
        request = lnrpc.SendManyRequest(
            AddrToAmount=AddrToAmount,
            target_conf=target_conf,
            sat_per_byte=sat_per_byte,
            label=label,
        )
        response = self._ln_stub.SendMany(request)
        return response

    # https://api.lightning.community/#sendpaymentsync
    def send_payments_sync(
        self,
        dest: bytes,
        dest_string: str,
        amt: int,
        amt_msat: int,
        pament_hash: bytes,
        payment_hash_string: str,
        payment_request: str,
        final_cltv_delta: int,
        fee_limit,
        outgoing_chan_id: int,
        last_hop_pubkey: bytes,
        cltv_limit: int,
        dest_custom_records,
        allow_self_payment: bool,
        dest_features):
        request = lnrpc.SendRequest(
            dest=dest,
            dest_string=dest_string,
            amt=amt,
            amt_msat=amt_msat,
            payment_hash=payment_hash,
            payment_hash_string=payment_hash_string,
            payment_request=payment_request,
            final_cltv_delta=final_cltv_delta,
            fee_limit=fee_limit,
            outgoing_chan_id=outgoing_chan_id,
            last_hop_pubkey=last_hop_pubkey,
            cltv_limit=cltv_limit,
            dest_custom_records=dest_custom_records,
            allow_self_payment=allow_self_payment,
            dest_features=dest_features,
        )
        response = self._ln_stub.SendPaymentSync(request)
        return response


    def subscribe_channel_balance(self):
        response = self._ln_stub.SubscribeChannelBackups(lnrpc.ChannelBackupSubscription())
        return response

    

    # https://api.lightning.community/#walletbalance
    def wallet_balance(self):
        response = self._ln_stub.WalletBalance(lnrpc.WalletBalanceRequest()) 
        return response

    '''
    def forwarding_history(self):
        request = lnrpc.ForwardingHistoryRequest(
        start_time=<uint64>,
        end_time=<uint64>,
        index_offset=<uint32>,
        num_max_events=<uint32>,
        )
        response = self.ln_stub.FeeReport(lnrpc.FeeReportRequest())
        return response
    '''